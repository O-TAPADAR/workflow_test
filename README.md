# Workflow Assignment

This project extracts text from images using Optical Character Recognition (OCR) and groups the extracted words into sentences or items using a Large Language Model (LLM). 

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Overview

This application takes an image as input and performs the following steps:

1. Extracts text, its position, and confidence score from the image using **pytesseract** (OCR).
2. Sends the extracted text and its coordinates to OpenAI's GPT-4 model to group the words into sentences based on their meaning.
3. Outputs the results in a structured DataFrame format containing:
   - Word
   - X, Y coordinates
   - Confidence level
   - Identifier

## Requirements

The following dependencies are required to run the project:

- `pytesseract`: For extracting text from images using OCR.
- `opencv-python`: For image loading and processing.
- `pandas`: For structuring the output as a DataFrame.
- `openai`: For interacting with OpenAI's GPT models.

### Additional Tools
- Tesseract OCR engine needs to be installed on your system. You can install it using the following:
  - **macOS**: `brew install tesseract`
  - **Linux**: `sudo apt-get install tesseract-ocr`
  - **Windows**: [Download from here](https://github.com/tesseract-ocr/tesseract/wiki)

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/O-TAPADAR/workflow_test.git
    ```

2. Navigate to the project directory:
    ```bash
    cd workflow_test
    ```

3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up your OpenAI API key:
    - Create an `.env` file or set your API key directly in your script.
    - You can get your OpenAI API key from [OpenAI's API platform](https://beta.openai.com/signup/).

## Usage

To run the script on an image:

1. Place the image file in the `assets` folder (or provide the path to your own image).

2. Run the script:

    ```bash
    python main.py
    ```

3. The output will be a pandas DataFrame that contains the extracted words, their coordinates, confidence levels, and sentence/group identifiers assigned by the LLM.

### Example:
```bash
   word    x      y  confidence identifier
0  Help   130    50      95       1
1  Center 150    100     90       1
2  GoPay  120    200     85       2
