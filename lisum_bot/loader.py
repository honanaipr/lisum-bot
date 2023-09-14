"""
This file contain all global objects for bit,
to avoid circular imports.
"""
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from lisum_bot.config import config

storage: BaseStorage
if config.redis.host and config.redis.port:
    from aiogram.fsm.storage.redis import (
        DefaultKeyBuilder,
        RedisEventIsolation,
        RedisStorage,
    )
    from redis.asyncio import Redis

    redis = Redis(host=config.redis.host, port=config.redis.port)
    key_builder = DefaultKeyBuilder(with_destiny=True)
    storage = RedisStorage(redis=redis, key_builder=key_builder)
    event_isolation = RedisEventIsolation(redis=redis, key_builder=key_builder)
    logger.info(f"redis host: {config.redis.host}, redis port: {config.redis.port}")
elif config.redis.url:
    from aiogram.fsm.storage.redis import (
        DefaultKeyBuilder,
        RedisEventIsolation,
        RedisStorage,
    )
    from redis.asyncio import Redis

    redis = Redis.from_url(url=config.redis.url)
    key_builder = DefaultKeyBuilder(with_destiny=True)
    storage = RedisStorage.from_url(redis=redis, key_builder=key_builder)
    event_isolation = RedisEventIsolation(redis=redis, key_builder=key_builder)
    logger.info(f"redis url: {config.redis.url}")
else:
    from aiogram.fsm.storage.memory import (
        BaseEventIsolation,  # noqa: F811
        MemoryStorage,  # noqa: F811
    )

    storage = MemoryStorage()
    event_isolation = BaseEventIsolation()

bot = Bot(token=config.bot.token)
dp = Dispatcher(storage=MemoryStorage(), events_isolation=event_isolation)

@dp.startup()
def on_start():
    logger.info(f"Started")
