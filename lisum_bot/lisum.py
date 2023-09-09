import asyncio

import httpx
from pydantic import BaseModel, Field

from lisum_bot.config import config
from lisum_bot.exceptions import LisumError

BASE_URL: str = str(config.lisum.url)
TIMEOUT: int = config.lisum.timeout

class BaseRequest(BaseModel):
    id: int


class DialogueRequest(BaseRequest):
    question: str


class ReplyRequest(DialogueRequest):
    reply_id: int


class ReactionRequest(BaseModel):
    reaction_emoji: str = Field(serialization_alias="reactionEmoji")


async def dialog_request(id: int, question: str, reply_id: int | None = None) -> str:
    try:
        async with httpx.AsyncClient() as client:
            if reply_id is not None:
                request_data = ReplyRequest(id=id, question=question, reply_id=reply_id)
            else:
                request_data = DialogueRequest(id=id, question=question)
            response = await client.post(
                BASE_URL, json=request_data.dict(), timeout=TIMEOUT
            )
            if response.status_code == 200:
                return response.json()["post"]["answer"]
            else:
                raise LisumError(f"{response.status_code} {response.text}")
    except Exception as exp:
        raise LisumError from exp


async def reaction_request(id: int, reaction: str) -> None:
    try:
        async with httpx.AsyncClient() as client:
            request_data = ReactionRequest(reaction_emoji=reaction)
            response = await client.patch(
                BASE_URL.rstrip("/") + f"/{id}", json=request_data.dict(), timeout=TIMEOUT
            )
            if response.status_code == 200:
                return response.json()["post"]["answer"]
            else:
                raise LisumError(f"{response.status_code} {response.text}")
    except Exception as exp:
        raise LisumError from exp
