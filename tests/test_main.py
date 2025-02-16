import pytest
from httpx import AsyncClient
from app.main import app
from app.database.data_utils import db

@pytest.fixture(autouse=True, scope="function")
async def clear_db():
    # Clear the products and orders collections before each test.
    await db.products.delete_many({})
    await db.orders.delete_many({})
    yield

@pytest.mark.asyncio
async def test_create_and_get_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create a new product
        product_payload = {
            "name": "Test Product",
            "description": "A product for testing",
            "price": 19.99,
            "stock": 10
        }
        create_response = await ac.post("/api/addproducts", json=product_payload)
        assert create_response.status_code == 201
        created_product = create_response.json()
        assert created_product["name"] == product_payload["name"]

        # Retrieve products
        get_response = await ac.get("/api/getproducts")
        assert get_response.status_code == 200
        products = get_response.json()
        assert len(products) == 1
        assert products[0]["name"] == product_payload["name"]

@pytest.mark.asyncio
async def test_place_order_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create two products
        product1 = {"name": "Product 1", "description": "Desc 1", "price": 10.0, "stock": 5}
        product2 = {"name": "Product 2", "description": "Desc 2", "price": 20.0, "stock": 3}
        res1 = await ac.post("/api/addproducts", json=product1)
        res2 = await ac.post("/api/addproducts", json=product2)
        prod1 = res1.json()
        prod2 = res2.json()

        # Place an order using both products
        order_payload = {
            "products": [
                {"product_id": prod1["id"], "quantity": 2},
                {"product_id": prod2["id"], "quantity": 1}
            ]
        }
        order_response = await ac.post("/api/orders", json=order_payload)
        assert order_response.status_code == 201
        order_data = order_response.json()
        expected_total = product1["price"] * 2 + product2["price"] * 1
        assert order_data["total_price"] == expected_total
        assert order_data["status"] == "completed"

@pytest.mark.asyncio
async def test_place_order_insufficient_stock():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create a product with limited stock
        product = {"name": "Limited Stock", "description": "Limited", "price": 15.0, "stock": 1}
        res = await ac.post("/api/addproducts", json=product)
        prod = res.json()

        # Attempt to order more than is available
        order_payload = {
            "products": [
                {"product_id": prod["id"], "quantity": 2}
            ]
        }
        order_response = await ac.post("/api/orders", json=order_payload)
        assert order_response.status_code == 400
        error_data = order_response.json()
        assert "Insufficient stock" in error_data["detail"]