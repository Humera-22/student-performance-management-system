# app/utils.py
import redis
import json
from datetime import datetime
from app.config import Config

class Utils:
    """Common utility functions for caching and datetime formatting"""

    # Redis client shared across the app
    redis_client = redis.Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        db=Config.REDIS_DB,
        decode_responses=True
    )

    @staticmethod
    def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Convert datetime object to string"""
        return dt.strftime(fmt)

    @classmethod
    def get_cache(cls, key: str):
        """Fetch data from Redis cache"""
        try:
            value = cls.redis_client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            print(f"Redis GET error: {e}")
            return None

    @classmethod
    def set_cache(cls, key: str, value, expiry: int = 60):
        """Store data in Redis cache with optional expiry"""
        try:
            cls.redis_client.setex(key, expiry, json.dumps(value))
        except Exception as e:
            print(f"Redis SET error: {e}")

    @classmethod
    def delete_cache(cls, key: str):
        """Delete key from Redis cache"""
        try:
            cls.redis_client.delete(key)
        except Exception as e:
            print(f"Redis DELETE error: {e}")
