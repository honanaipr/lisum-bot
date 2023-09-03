import asyncio
from collections.abc import Generator

# import openai
# import requests
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from loguru import logger

from lisum_bot import lisum
# from tele_gpt.gpt import get_gpt_stream
from lisum_bot.states import Chat

chat_router = Router()

task_pool: set[asyncio.Task] = set()


@chat_router.message(Command("state"))
async def command_state(message: Message, state: FSMContext) -> None:
    await message.answer(
        str(await state.get_state()),
        reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
    )


@chat_router.message(Command(commands=["start", "cancel", "help"]))
async def command_start(
    message: Message, state: FSMContext, command: CommandObject
) -> None:
    if command.command in ["start", "help"]:
        await message.answer(
            "banner",
            reply_markup=ReplyKeyboardRemove(),
        )
    if command.command in ["start", "cancel"]:
        await state.set_state(Chat.waiting_message)
        await message.answer(
            "Начинайте диалог",
            reply_markup=ReplyKeyboardRemove(),
        )


# @chat_router.message(Chat.waiting_role, F.text)
# async def role_handler(message: Message, state: FSMContext) -> None:
#     await state.set_state(Chat.waiting_message)
#     messages = [
#         {
#             "role": "system",
#             "content": message.text,
#         }
#     ]
#     await state.update_data(messages=messages)
#     await message.answer(
#         "Начинайте чат:",
#         reply_markup=ReplyKeyboardRemove(),
#     )


# async def chat_task(stream: Generator, message: Message, state: FSMContext):
#     try:
#         async with asyncio.timeout(100):
#             chunks_queue = []
#             preamble = "Печатает...\n"
#             message_text = ""
#             try:
#                 for chunk in stream:
#                     if chunk["choices"][0]["finish_reason"] != "stop":
#                         chunks_queue.append(chunk["choices"][0]["delta"]["content"])
#                         if len(chunks_queue) > 50:
#                             message_text += "".join(chunks_queue)
#                             chunks_queue.clear()
#                             await message.edit_text(preamble + message_text)
#                     await asyncio.sleep(0)
#             except (openai.error.APIError, requests.exceptions.RequestException) as exc:
#                 logger.debug("Open ai stream error")
#                 await message.answer("Модель перегружена. Попробуйте позже")
#                 await message.answer(str(exc))
#                 await state.set_state(Chat.waiting_role)
#                 await message.answer(
#                     "Введите роль",
#                     reply_markup=ReplyKeyboardRemove(),
#                 )
#                 task = asyncio.current_task()
#                 if task:
#                     task_pool.remove(task)
#                 return
#             if chunks_queue:
#                 message_text += "".join(chunks_queue)
#                 await message.edit_text(message_text)
#             data = await state.get_data()
#             messages = data["messages"]
#             messages.append({"role": "assistant", "content": message_text})
#             await state.update_data(messages=messages)
#             await state.set_state(Chat.waiting_message)
#             if task:
#                 task_pool.remove(task)
#             logger.debug("Task ended normaly")
#     except TimeoutError:
#         logger.debug("Timeout")
#         await message.answer("Модель перегружена. Попробуйте позже")
#         await state.set_state(Chat.waiting_role)
#         await message.answer(
#             "Введите роль",
#             reply_markup=ReplyKeyboardRemove(),
#         )
#         if task:
#             task_pool.remove(task)
#         return


@chat_router.message(Chat.processing_message)
async def message_deleter(message: Message, state: FSMContext) -> None:
    await message.delete()


@chat_router.message(Chat.waiting_message, F.text)
async def message_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Chat.processing_message)
    answer = await message.answer("Печатает...")
    if message.reply_to_message:
        response = await lisum.send_request(id=hash((message.chat.id, message.message_id)), question=message.text, reply_id=message.reply_to_message.id)
    else:
        response = await lisum.send_request(id=hash((message.chat.id, message.message_id)), question=message.text)
    await answer.edit_text(response)
    await state.set_state(Chat.waiting_message)

