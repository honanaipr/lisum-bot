import asyncio

import httpx
from pydantic import BaseModel

BASE_URL = "http://91.236.197.244:8080/api/v1/dialogue/"

class DialogueRequest(BaseModel):
    id: int
    question: str
class DialogueRequestWithReply(DialogueRequest):
    reply_id: int

class DialogueResponse(BaseModel):
    id: int
    answer: str
    time_create: str
    time_update: str
    question: str


async def send_request(id: int, question: str, reply_id: int | None = None) -> str:
    async with httpx.AsyncClient() as client:
        if reply_id is not None:
            request_data = DialogueRequestWithReply(id=id, question=question, reply_id=reply_id)
        else:
            request_data = DialogueRequest(id=id, question=question)
        response = await client.post(
            BASE_URL,
            json=request_data.dict(),
            timeout=None
        )
        if response.status_code == 200:
            return response.json()['post']['answer']
        else:
            return f"{response.status_code} {response.text}"
