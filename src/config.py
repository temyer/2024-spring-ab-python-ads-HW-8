import typing as tp
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    REDIS_HOST: tp.Final[str] = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT: tp.Final[int] = os.environ.get("REDIS_PORT", 6379)
    REDIS_PWD: tp.Final[str] = os.environ.get("REDIS_PWD", "admin")
    RABBIT_HOST: tp.Final[str] = os.environ.get("RABBIT_HOST", "localhost")
    RABBIT_PORT: tp.Final[int] = os.environ.get("RABBIT_PORT", 5672)
    RABBIT_USER: tp.Final[str] = os.environ.get("RABBIT_USER", "admin")
    RABBIT_PWD: tp.Final[str] = os.environ.get("RABBIT_PWD", "admin")


@lru_cache
def get_config():
    return Config()
