from pydantic import BaseModel
from typing import Optional



# Shared Base
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int


# Request Schemas

class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


# Response Schema
class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
