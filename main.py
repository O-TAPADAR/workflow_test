import pytesseract
import cv2
import pandas as pd
import openai 

# Settings
openai.api_key = ""                         #TODO: INSERT YOUR OPEN AI API KEY HERE
IMAGE_URL = "assets/Gojek Android 409.png"

# Step 1: Load Image and Apply OCR
def ocr_image(image_path):
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    ocr_data = pytesseract.image_to_data(rgb_image, output_type=pytesseract.Output.DICT)
    
    return ocr_data

# Step 2: Extract Coordinates, Text, Confidence
def extract_text_and_coordinates(ocr_data):
    words = []
    coordinates = []
    confidences = []
    
    n_boxes = len(ocr_data['level'])
    for i in range(n_boxes):
        text = ocr_data['text'][i].strip()
        if text:  
            words.append(text)
            x = ocr_data['left'][i]
            y = ocr_data['top'][i]
            w = ocr_data['width'][i]
            h = ocr_data['height'][i]
            coordinates.append((x, y, w, h))
            confidences.append(float(ocr_data['conf'][i]))
    
    return words, coordinates, confidences

# Step 3: Process Text with an LLM
def group_text_with_openai(words, coordinates, confidences):
    # Prepare the OCR output for the LLM input
    ocr_input = "\n".join([f"Word: '{word}', Coordinates: {coord}" for word, coord in zip(words, coordinates)])
    
    messages = [
    {
        "role": "user",
        "content": (
            "Here are words extracted from an image along with their coordinates:\n"
            f"{ocr_input}\n\n"
            "Please group the words into sentences or items based on their meaning. "
            "Return a unique identifier (Sentence ID) for each group of words. "
            "Please return the response in this structured format:\n"
            "Word: [word], Sentence ID: [sentence_id]\n"
            "Make sure there are no extra quotes or special characters, and ensure each line only contains one word and its corresponding Sentence ID."
            )
        }
    ]
    
    # Call the OpenAI API using chat completion
    chat_completion = openai.chat.completions.create(
        messages=messages,
        model="gpt-4", 
    )
    
    # Extract the response content from the API call
    response_text = chat_completion.choices[0].message.content.strip()
    groupings = response_text.split("\n")

    # Extract ids
    identifiers = []

    for group in groupings: 
        _, id_part = group.split(", Sentence ID: ")
        identifiers.append(id_part)
    
    return identifiers

# Step 4: Structure Output
def create_output(words, coordinates, confidences, identifiers):
    output_data = []
    
    for word, (x, y, w, h), confidence, identifier in zip(words, coordinates, confidences, identifiers):
        x_center = x + w / 2  
        y_center = y + h / 2
        
        output_data.append({
            "word": word,
            "x": x_center,
            "y": y_center,
            "confidence": confidence,
            "identifier": identifier
        })
    
    df = pd.DataFrame(output_data)
    return df

# Main function to process the image
def process_image(image_path):
    # Step 1: OCR to get text and coordinates
    ocr_data = ocr_image(image_path)
    
    # Step 2: Extract words, coordinates, and confidence levels
    words, coordinates, confidences = extract_text_and_coordinates(ocr_data)

    # Step 3: Extract identifiers using an LLM.
    identifiers = group_text_with_openai(words, coordinates, confidences)

    # Step 4: Prepare the output
    df = create_output(words, coordinates, confidences, identifiers)

    return df



# Main
result_df = process_image(IMAGE_URL)
print(result_df)