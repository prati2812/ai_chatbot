from app.providers.factory import ProviderFactory
from app.providers.base import AIProvider
from app.services.chat_service import ChatService
from app.services.context_manager import ContextManager
from app.builders.prompt_builder import PromptBuilder
from app.services.memory_service import MemoryService
from app.core.config import settings

from fastapi import Depends 

# Singleton instance of memory service to persist state across requests
memory_service_instance = MemoryService()

def get_ai_provider() -> AIProvider:
    return ProviderFactory.get_provider(settings.default_provider)

def get_prompt_builder() -> PromptBuilder:
    return PromptBuilder()

def get_memory_service() -> MemoryService:
    return memory_service_instance

def get_chat_service(
    provider: AIProvider = Depends(get_ai_provider),
    prompt_builder: PromptBuilder = Depends(get_prompt_builder),
    memory_service: MemoryService = Depends(get_memory_service),
    context_manager: ContextManager = Depends(get_context_manager)
) -> ChatService:
    return ChatService(provider, prompt_builder, memory_service, context_manager)

def get_context_manager() -> ContextManager:
    return ContextManager(
        settings.max_history_messages
    )    