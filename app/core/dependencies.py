from app.providers.factory import ProviderFactory
from app.providers.base import AIProvider
from app.services.chat_service import ChatService
from app.core.config import settings

from fastapi import Depends 

def get_ai_provider() -> AIProvider:
    return ProviderFactory.get_provider(settings.default_provider)

def get_chat_service(
    provider: AIProvider = Depends(get_ai_provider)
) -> ChatService:
    return ChatService(provider)    