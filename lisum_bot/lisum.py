import asyncio

import httpx
from pydantic import BaseModel, Field

from lisum_bot.config import config
from lisum_bot.exceptions import LisumError

BASE_URL: str = str(config.lisum.url)
TIMEOUT: int = None  # config.lisum.timeout


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
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            if reply_id is not None:
                request_data = ReplyRequest(id=id, question=question, reply_id=reply_id)
            else:
                request_data = DialogueRequest(id=id, question=question)
            response = await client.post(
                "/", json=request_data.dict(by_alias=True), timeout=TIMEOUT
            )
    except Exception as exp:
        raise LisumError(exp)
    if response.status_code == 200:
        try:
            return response.json()["post"]["answer"]
        except KeyError as exp:
            LisumError(exp)
    else:
        raise LisumError(f"{response.status_code} {response.text}")


async def reaction_request(id: int, reaction: str) -> None:
    try:
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            request_data = ReactionRequest(reaction_emoji=reaction)
            response = await client.patch(
                f"/{id}",
                json=request_data.model_dump(by_alias=True),
                timeout=TIMEOUT,
            )
    except Exception as exp:
        raise LisumError(exp)
    if response.status_code != 200:
        raise LisumError(f"{response.status_code} {response.text}")
