import redis.asyncio as redis

from app.core.config import get_settings


def connect_redis_pool(settings: dict = get_settings()) -> redis.ConnectionPool:
    try:
        return redis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=10)
    except redis.exceptions.ConnectionError as e:
        raise ConnectionError(f"Failed to connect to Redis: {e}")
