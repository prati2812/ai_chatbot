from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.chat_service import ChatService
from app.core.dependencies import get_chat_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str 

@router.post("/chat")
async def chat(
      request: ChatRequest,
      chat_service: ChatService = Depends(get_chat_service)
):
    return StreamingResponse(
        chat_service.chat(request.message),
        media_type="text/plain"
    )
