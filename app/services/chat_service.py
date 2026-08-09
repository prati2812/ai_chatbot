from app.providers.base import AIProvider
from app.builders.prompt_builder import PromptBuilder
from app.services.memory_service import MemoryService
from app.services.context_manager import ContextManager
from app.services.token_manager import TokenManager
from app.parsers.output_parser import OutputParser
from app.executors.tool_executor import ToolExecutor

class ChatService:
    def __init__(self, provider: AIProvider, prompt_builder: PromptBuilder, memory_service: MemoryService, context_manager: ContextManager, token_manager: TokenManager, output_parser: OutputParser, tool_executor: ToolExecutor):
        self.provider = provider
        self.prompt_builder = prompt_builder
        self.memory_service = memory_service
        self.context_manager = context_manager
        self.token_manager = token_manager
        self.output_parser = output_parser
        self.tool_executor = tool_executor
        
    async def chat(self, conversation_id: str, user_message: str):
        # 1. Save the new user message to memory FIRST
        self.memory_service.save_user_message(conversation_id, user_message)

        # 2. Load history (which now includes the user's message)
        history = self.memory_service.load_history(conversation_id)

        selected_history = self.context_manager.get_context(history)
        
        # 3. Build the full prompt (system + history)
        messages = self.prompt_builder.build(selected_history)

        # 4. Prepare messages to fit token limits
        messages = self.token_manager.prepare(messages)

        # 5. Stream response from provider
        stream = self.provider.chat(messages)
        
        # 5. Intercept the stream to accumulate and save the assistant's message
        async def stream_and_save():
            full_response = ""
            try:
                async for chunk in stream:
                    full_response += chunk
                    yield chunk
                
                # 6. Save successful assistant message
                self.memory_service.save_assistant_message(conversation_id, full_response)
            except Exception as e:
                # 7. If failed, save failure status
                error_msg = f"[System Error: {str(e)}]"
                self.memory_service.save_assistant_message(conversation_id, error_msg)
                raise e

        return stream_and_save()
