import typing as tp

from redis.asyncio import Redis
from fastapi import Request, Depends

from src.config import get_config


async def setup_redis_client():
    config = get_config()

    redis = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PWD,
        decode_responses=True,
    )
    return redis


async def get_redis_client(request: Request):
    return request.app.state.redis


GetRedis = tp.Annotated[Redis, Depends(get_redis_client)]
