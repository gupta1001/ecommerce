from fastapi import APIRouter
from app.src.models.product_details import (
    Product,
    ProductCreate,
    Order,
    OrderCreate
)
from app.src.services import product_service

router = APIRouter(prefix="/api")

@router.get("/getproducts", response_model=list[Product])
async def read_products():
    products = await product_service.get_products()
    return products

@router.post("/addproducts", response_model=Product, status_code=201)
async def add_product(product: ProductCreate):
    print(product)
    created_product = await product_service.create_product(product)
    return created_product

@router.post("/orders", response_model=Order, status_code=201)
async def place_order(order: OrderCreate):
    created_order = await product_service.create_order(order)
    return created_order