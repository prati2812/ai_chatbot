from app.providers.factory import ProviderFactory
from app.providers.base import AIProvider
from app.services.chat_service import ChatService
from app.services.context_manager import ContextManager
from app.builders.prompt_builder import PromptBuilder
from app.parsers.output_parser import OutputParser
from app.services.memory_service import MemoryService
from app.services.token_manager import TokenManager
from app.executors.tool_executor import ToolExecutor
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

def get_context_manager() -> ContextManager:
    return ContextManager(
        settings.max_history_messages
    )

def get_token_manager() -> TokenManager:
    return TokenManager()

def get_output_parser() -> OutputParser:
    return OutputParser()

def get_tool_executor() -> ToolExecutor:
    return ToolExecutor()

def get_chat_service(
    provider: AIProvider = Depends(get_ai_provider),
    prompt_builder: PromptBuilder = Depends(get_prompt_builder),
    memory_service: MemoryService = Depends(get_memory_service),
    context_manager: ContextManager = Depends(get_context_manager),
    token_manager: TokenManager = Depends(get_token_manager),
    output_parser: OutputParser = Depends(get_output_parser),
    tool_executor: ToolExecutor = Depends(get_tool_executor)
) -> ChatService:
    return ChatService(provider, prompt_builder, memory_service, context_manager, token_manager, output_parser, tool_executor)