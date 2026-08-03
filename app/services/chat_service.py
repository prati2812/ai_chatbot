from app.providers.base import AIProvider
from app.builders.prompt_builder import PromptBuilder
from app.services.memory_service import MemoryService

class ChatService:
    def __init__(self, provider: AIProvider, prompt_builder: PromptBuilder, memory_service: MemoryService):
        self.provider = provider
        self.prompt_builder = prompt_builder
        self.memory_service = memory_service
        
    async def chat(self, conversation_id: str, user_message: str):
        # 1. Save the new user message to memory FIRST
        self.memory_service.save_user_message(conversation_id, user_message)

        # 2. Load history (which now includes the user's message)
        history = self.memory_service.load_history(conversation_id)
        
        # 3. Build the full prompt (system + history)
        messages = self.prompt_builder.build(history)

        # 4. Stream response from provider
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
