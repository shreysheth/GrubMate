from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class OrderItem(BaseModel):
    name: str = Field(..., description="Name of the menu item")
    quantity: int = Field(..., description="Quantity ordered")
    price: float = Field(..., description="Price per item")

class Order(BaseModel):
    user_id: str = Field(..., description="Unique identifier of the user")
    items: List[OrderItem] = Field(..., description="List of ordered items")
    total_price: float = Field(..., description="Total cost of the order")
    status: str = Field(..., description="Order status like pending, completed, etc.")
    created_at: datetime = Field(..., description="Timestamp of when the order was created")