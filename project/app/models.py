from pydantic import BaseModel
from typing import Optional

class Expense(BaseModel):
    id: Optional[int] = None
    date: str
    amount: float
    description: str
    category: str

class Receipt(BaseModel):
    file_name: str
    expense: Expense
