# API routes for chat
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.ollama_service import OllamaService
from app.core.dependencies import get_ollama_service

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest, ollama_service: OllamaService = Depends(get_ollama_service)):
    return StreamingResponse(
        ollama_service.chat(request.message),
        media_type="application/x-ndjson"
    )
