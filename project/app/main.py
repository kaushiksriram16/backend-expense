from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import os
import json
from uuid import uuid4
from app.models import Expense
from app.ocr_processing import process_receipt, categorize_receipt_ml
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins (for development only; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory expense storage (as before)
expenses = [
    {"id": 1, "date": "2024-12-01", "amount": 120.5, "description": "Grocery shopping at Walmart", "category": "Groceries"},
    {"id": 2, "date": "2024-12-02", "amount": 35.0, "description": "Uber ride to downtown", "category": "Transport"},
    {"id": 3, "date": "2024-12-03", "amount": 15.99, "description": "Dinner at a local restaurant", "category": "Dining"},
    {"id": 4, "date": "2024-12-04", "amount": 49.99, "description": "Monthly Netflix subscription", "category": "Entertainment"},
    {"id": 5, "date": "2024-12-05", "amount": 75.25, "description": "Electricity bill payment", "category": "Utilities"},
    {"id": 6, "date": "2024-12-05", "amount": 20.0, "description": "Coffee shop visit", "category": "Dining"},
]

# Store and load expenses from JSON file
def save_expenses():
    with open("app/data.json", "w") as f:
        json.dump(expenses, f)

def load_expenses():
    global expenses
    if os.path.exists("app/data.json"):
        with open("app/data.json", "r") as f:
            expenses = json.load(f)

load_expenses()

@app.get("/expenses/", response_model=List[Expense])
def get_expenses():
    return expenses

@app.post("/expenses/add/", response_model=Expense)
def add_expense(expense: Expense):
    expense.id = len(expenses) + 1
    expenses.append(expense.dict())
    save_expenses()
    return expense

@app.delete("/expenses/{expense_id}/")
def delete_expense(expense_id: int):
    global expenses
    expenses = [expense for expense in expenses if expense["id"] != expense_id]
    save_expenses()
    return JSONResponse(content={"message": "Expense deleted successfully!"}, status_code=200)

@app.post("/upload/")
async def upload_receipt(file: UploadFile = File(...)):
    try:
        # Save the uploaded receipt file
        file_location = f"receipts/{uuid4()}_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        
        # Process OCR and use ML model for categorization
        ocr_text, _ = process_receipt(file_location)  # OCR processing here
        category = categorize_receipt_ml(ocr_text)  # Categorization using ML model

        # Create new expense from OCR data and ML category
        new_expense = Expense(
            date="2024-12-06",  # You can extract date from OCR text if needed
            amount=45.5,  # Set based on OCR text extraction
            description=ocr_text,  # OCR description
            category=category  # Categorized using ML
        )

        # Add new expense to in-memory storage
        add_expense(new_expense)

        return {"message": "Receipt uploaded and expense created", "expense": jsonable_encoder(new_expense)}

    except Exception as e:
        return {"error": str(e)}
