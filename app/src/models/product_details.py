from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str


class OrderItem(BaseModel):
    product_id: str
    quantity: int

class OrderBase(BaseModel):
    products: List[OrderItem]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: str
    total_price: float
    status: str