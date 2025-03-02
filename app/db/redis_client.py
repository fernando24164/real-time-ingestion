import redis.asyncio as aioredis
from redis.exceptions import ConnectionError

from app.core.config import get_settings


def connect_redis_pool(settings: dict = get_settings()) -> aioredis.ConnectionPool:
    try:
        return aioredis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=10)
    except ConnectionError as e:
        raise ConnectionError(f"Failed to connect to Redis: {e}")
