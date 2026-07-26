# Pydantic schemas for chat
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str