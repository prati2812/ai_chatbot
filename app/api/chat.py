from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services.chat_service import ChatService
from app.core.dependencies import get_chat_service
from app.schemas.chat import ChatRequest

router = APIRouter()
@router.post("/chat")
async def chat(
      request: ChatRequest,
      chat_service: ChatService = Depends(get_chat_service)
):
    response = await chat_service.chat(request.conversation_id, request.message)
    return {"response": response}
