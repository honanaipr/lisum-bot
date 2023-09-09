"""
This file contain validation template for
bot's configuratin, given from environ.
"""

from loguru import logger
from pydantic import (
    AnyHttpUrl,
    BaseModel,
    Field,
    RedisDsn,
    ValidationError,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseModel):
    token: str = Field(pattern="^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$")


class LisumConfig(BaseModel):
    url: AnyHttpUrl
    timeout: int


class Settings(BaseSettings):
    bot: BotConfig
    redis: RedisDsn = Field("redis://localhost:6379/db")
    lisum: LisumConfig

    model_config = SettingsConfigDict(env_nested_delimiter="_", env_file=".env")


try:
    config = Settings()
except ValidationError as exc:
    logger.error(exc)
    quit(1)
