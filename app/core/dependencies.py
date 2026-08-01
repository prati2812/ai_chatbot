from app.providers.factory import ProviderFactory
from app.providers.base import AIProvider
from app.services.chat_service import ChatService
from app.builders.prompt_builder import PromptBuilder
from app.core.config import settings

from fastapi import Depends 

def get_ai_provider() -> AIProvider:
    return ProviderFactory.get_provider(settings.default_provider)

def get_prompt_builder() -> PromptBuilder:
    return PromptBuilder()

def get_chat_service(
    provider: AIProvider = Depends(get_ai_provider),
    prompt_builder: PromptBuilder = Depends(get_prompt_builder)
) -> ChatService:
    return ChatService(provider, prompt_builder)