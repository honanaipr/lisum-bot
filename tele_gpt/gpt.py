import asyncio
import os
from collections.abc import Generator

import openai

openai.api_key = "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"


def get_gpt_stream(
    *, role: str = "", message: str | None = None, messages: list | None = None
) -> Generator:
    if not messages:
        messages = [
            {"role": "system", "content": role},
            {"role": "user", "content": message},
        ]
    stream = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, stream=True
    )
    return stream
