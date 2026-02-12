import redis
import json
from config import Config

redis_client = None

def init_cache():
    """Initialize Redis connection"""
    global redis_client
    try:
        redis_client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            decode_responses=True
        )
        redis_client.ping()
        print(f"Connected to Redis at {Config.REDIS_HOST}:{Config.REDIS_PORT}")
        return redis_client
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        print("Analytics will run without caching")
        return None

def get_cache(key):
    """Get value from cache"""
    if not redis_client:
        return None
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Cache get error: {e}")
        return None

def set_cache(key, value, ttl=None):
    """Set value in cache"""
    if not redis_client:
        return False
    try:
        ttl = ttl or Config.CACHE_TTL
        redis_client.setex(key, ttl, json.dumps(value))
        return True
    except Exception as e:
        print(f"Cache set error: {e}")
        return False

def delete_cache(pattern):
    """Delete cache keys matching pattern"""
    if not redis_client:
        return False
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True
    except Exception as e:
        print(f"Cache delete error: {e}")
        return False

def close_cache():
    """Close Redis connection"""
    if redis_client:
        redis_client.close()
        print("Redis connection closed")
