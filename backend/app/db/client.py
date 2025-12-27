"""
MongoDB database client
"""
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

from app.core.config import settings


class MongoDBClient:
    """MongoDB client singleton"""

    client: Optional[AsyncIOMotorClient] = None
    database = None

    @classmethod
    async def connect(cls):
        """Connect to MongoDB"""
        if cls.client is None:
            cls.client = AsyncIOMotorClient(settings.mongodb_uri)
            db_name = settings.mongodb_uri.split("/")[-1].split("?")[0]
            cls.database = cls.client[db_name]
            # Test connection
            try:
                await cls.client.admin.command("ping")
            except ConnectionFailure:
                raise ConnectionFailure("Failed to connect to MongoDB")

    @classmethod
    async def disconnect(cls):
        """Disconnect from MongoDB"""
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.database = None

    @classmethod
    def get_database(cls):
        """Get database instance"""
        return cls.database

