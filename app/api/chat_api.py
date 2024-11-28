from fastapi import APIRouter
from app.api.schemas.chat_schema import ChatRequestPayload
from app.configs import log
from app.common.utilis import current_time_in_ms
from app.api.chat_api_service import chat_with_ai

from app.api.schemas.chat_schema import ChatRequestPayload
from app.configs import log
from app.common.utilis import current_time_in_ms


api = APIRouter(prefix="")

@api.post("/chat")
async def chat(payload: ChatRequestPayload):
    time = current_time_in_ms()
    log.info(f'Start: chat for userId: {payload.user_details.user_id} and threadId: {payload.user_details.thread_id}')

    response = chat_with_ai(payload)

    log.info(f'End: chat for userId: {payload.user_details.user_id} and threadId: {payload.user_details.thread_id} in {current_time_in_ms() - time} ms')
    return response