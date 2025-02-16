from fastapi import HTTPException, status
from app.src.models.product_details import (
    ProductCreate,
    OrderCreate
)
from app.database.data_utils import db
from bson.objectid import ObjectId

async def get_products():
    products_objs = db.products.find()
    products = []
    async for product in products_objs:
        print(product)
        product["id"] = str(product["_id"])
        del product["_id"]
        products.append(product)
    return products

async def create_product(product: ProductCreate):
    product_dict = product.model_dump()
    result = await db.products.insert_one(product_dict)
    created_product = await db.products.find_one({"_id": result.inserted_id})
    created_product["id"] = str(created_product["_id"])
    del created_product["_id"]
    return created_product

async def create_order(order: OrderCreate):
    total_price = 0.0
    order_items = order.products

    # validation of product and quantity
    for item in order_items:
        product = await db.products.find_one({"_id": ObjectId(item.product_id)})
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found."
            )
        if product["stock"] < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product id {item.product_id}."
            )
        total_price += product["price"] * item.quantity


    for item in order_items:
        update_result = await db.products.update_one(
            {"_id": ObjectId(item.product_id), "stock": {"$gte": item.quantity}},
            {"$inc": {"stock": -item.quantity}}
        )
        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to update stock for product id {item.product_id}."
            )


    order_doc = {
        "products": [item.dict() for item in order_items],
        "total_price": total_price,
        "status": "completed"  # Order is completed if stock was sufficient
    }
    result = await db.orders.insert_one(order_doc)
    order_doc["id"] = str(result.inserted_id)
    return order_doc