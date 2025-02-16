from fastapi import FastAPI
from app.src.routers import product_router

app = FastAPI(title="E-Commerce Platform API")

app.include_router(product_router.router)