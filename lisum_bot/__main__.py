import asyncio
import logging
import sys

from aiogram import Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from loguru import logger

from lisum_bot.loader import bot, dp
from lisum_bot.routers import chat_router

dp.include_router(chat_router)


async def main():
    await dp.start_polling(bot)

class LoguruHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        # Отправляем лог в Loguru
        logger.log(record.levelname, log_entry, level="DEBUG")

if __name__ == "__main__":
    logging.getLogger().addHandler(LoguruHandler())
    logger.level("DEBUG")
    asyncio.run(main())
