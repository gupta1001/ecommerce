import os
from motor.motor_asyncio import AsyncIOMotorClient

# reading mongo db connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["ecommerce"]