import asyncio
import logging
import sys
from logging import LogRecord

from aiogram import Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from loguru import logger

from lisum_bot.loader import bot, dp
from lisum_bot.routers import chat_router

dp.include_router(chat_router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    # logging.getLogger().addHandler(LoguruHandler())
    logger.level("DEBUG")
    asyncio.run(main())
