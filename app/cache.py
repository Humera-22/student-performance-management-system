import redis
import json
from functools import wraps
from app.config import Config

# Initialize Redis client using config
redis_client = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    decode_responses=True
)

# -------------------------
# Basic cache get/set
# -------------------------
def get_cache(key):
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print(f"Redis GET error: {e}")
    return None

def set_cache(key, value, expiry=60):
    try:
        redis_client.setex(key, expiry, json.dumps(value))
    except Exception as e:
        print(f"Redis SET error: {e}")

# -------------------------
# Caching decorator for routes
# -------------------------
def cache_response(key, expiry=60):
    """
    Decorator to cache route responses.
    Usage:
        @cache_response("students", expiry=120)
        def get_students():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            cached = get_cache(key)
            if cached:
                return cached  # Return cached dict (Flask jsonify will handle)
            result = f(*args, **kwargs)
            set_cache(key, result, expiry)
            return result
        return wrapped
    return decorator
