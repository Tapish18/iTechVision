from pydantic import BaseModel
from typing import Optional,Literal



# Request Schemas
class OrderCreate(BaseModel):
    user_id:int
    product_id: int
    quantity: int


class OrderUpdate(BaseModel):
    status: Literal["CREATED", "SHIPPED", "DELIVERED", "CANCELLED"]



# Response Schema
class OrderResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    quantity: int
    status: Literal["CREATED", "SHIPPED", "DELIVERED", "CANCELLED"]

    class Config:
        from_attributes = True
