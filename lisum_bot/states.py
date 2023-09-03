"""
This file contain all states of bot's fsm,
to avoid circular imports.
"""
from aiogram.fsm.state import State, StatesGroup


class Chat(StatesGroup):
    waiting_message = State()
    processing_message = State()
