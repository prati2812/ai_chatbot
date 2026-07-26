# API routes for chat
from fastapi import APIRouter

from app.schemas.chat import ChatRequest

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    return{
        "message": request.message
    }

    
