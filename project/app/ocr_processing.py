import pytesseract
from PIL import Image
import os

# Function to process OCR and extract data from image
def process_receipt(file_path: str):
    try:
        img = Image.open(file_path)
        ocr_text = pytesseract.image_to_string(img)
        # In a real app, this would be more sophisticated and involve categorization
        return ocr_text
    except Exception as e:
        return str(e)
    

import pickle
import os

# Load the pretrained model
model = None

def load_model():
    global model
    if model is None:
        # Check if the model file exists
        if os.path.exists('C:/Users/kaush/OneDrive/Desktop/projects/smart-expense-tracker/backend-fastapi/project/app/expense_categorizer.pkl'):
            with open('C:/Users/kaush/OneDrive/Desktop/projects/smart-expense-tracker/backend-fastapi/project/app/expense_categorizer.pkl', 'rb') as model_file:
                model = pickle.load(model_file)
        else:
            raise FileNotFoundError("Model file not found!")

load_model()

# Function to categorize the receipt using the pretrained model
def categorize_receipt_ml(ocr_text: str):
    """Categorize receipt using the pretrained ML model"""
    # Process the OCR text if necessary (text cleaning can go here)
    # For now, we directly use the text
    
    # Predict the category using the pretrained model
    category = model.predict([ocr_text])[0]  # Assuming the model takes a list of texts for prediction
    
    return category

