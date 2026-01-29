# app/utils.py
from datetime import datetime
import json
import redis
from app.config import Config

class Utils:
    """Common utility functions for caching and date formatting"""

    redis_client = redis.Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        db=Config.REDIS_DB,
        decode_responses=True
    )

    @staticmethod
    def format_datetime(dt: datetime, fmt="%Y-%m-%d %H:%M:%S"):
        return dt.strftime(fmt)

    @classmethod
    def get_cache(cls, key):
        try:
            data = cls.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Redis GET error: {e}")
            return None

    @classmethod
    def set_cache(cls, key, value, expiry=60):
        try:
            cls.redis_client.setex(key, expiry, json.dumps(value))
        except Exception as e:
            print(f"Redis SET error: {e}")
