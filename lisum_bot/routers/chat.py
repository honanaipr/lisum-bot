import asyncio
import unicodedata
from collections.abc import Generator

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.filters.command import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from lisum_bot import lisum
from lisum_bot.exceptions import LisumError
from lisum_bot.states import Chat

chat_router = Router()

task_pool: set[asyncio.Task] = set()

builder = InlineKeyboardBuilder()
reactions = ["😠", "😕", "😐", "🙂", "😃"]
for reaction in reactions:
    builder.button(text=f"{reaction}", callback_data=unicodedata.name(reaction))
reactions_keyboard = builder.as_markup()


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


@chat_router.message(Chat.processing_message)
async def message_deleter(message: Message, state: FSMContext) -> None:
    await message.delete()


@chat_router.message(~StateFilter(Chat.processing_message), F.text)
async def message_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Chat.processing_message)
    try:
        answer = await message.reply("Печатает...")
        if message.reply_to_message:
            response = await lisum.dialog_request(
                id=hash((message.chat.id, message.message_id)),
                question=message.text,
                reply_id=hash(
                    (message.chat.id, (await state.get_data())["last_question_id"])
                ),
            )
        else:
            await state.update_data(last_question_id=message.message_id)
            response = await lisum.dialog_request(
                id=hash((message.chat.id, message.message_id)), question=message.text
            )
        await answer.edit_text(response[:4096], reply_markup=reactions_keyboard)
    except Exception as exp:
        print(exp)
        await answer.edit_text("Ошибка :(")
    finally:
        await state.set_state(Chat.waiting_message)


@chat_router.callback_query()
async def callback_query_handler(callback_query: CallbackQuery) -> None:
    try:
        await lisum.reaction_request(
            id=hash(
                (
                    callback_query.message.chat.id,
                    callback_query.message.reply_to_message.message_id,
                )
            ),
            reaction=callback_query.data,
        )
        await callback_query.message.delete_reply_markup()
    except Exception as exp:
        print(exp)
        await callback_query.message.reply("Ошибка :(")
