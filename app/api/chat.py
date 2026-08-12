import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.services.chat_service import ChatService
from app.core.dependencies import get_chat_service
from app.schemas.chat import ChatRequest
from app.events.stream_event import StreamEvent

router = APIRouter()

async def sse_format(generator):
    async for event in generator:
        if isinstance(event, StreamEvent):
            yield f"event: {event.type}\ndata: {json.dumps(event.data)}\n\n"
        else:
            yield f"event: message\ndata: {json.dumps(event)}\n\n"

@router.post("/chat")
async def chat(
      request: ChatRequest,
      chat_service: ChatService = Depends(get_chat_service)
):
    return StreamingResponse(
        sse_format(chat_service.chat(request.conversation_id, request.message)),
        media_type="text/event-stream"
    )
