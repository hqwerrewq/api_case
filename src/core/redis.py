from redis.asyncio import Redis
from src.core.config import settings

redis_client = Redis(
    host=settings.redis.REDIS_HOST,
    port=settings.redis.REDIS_PORT,
    password=settings.redis.REDIS_PASSWORD,
    decode_responses=True
)