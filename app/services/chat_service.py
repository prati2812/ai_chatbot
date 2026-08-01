from app.providers.base import AIProvider
from app.builders.prompt_builder import PromptBuilder
from app.services.memory_service import MemoryService

class ChatService:
    def __init__(self, provider: AIProvider, prompt_builder: PromptBuilder, memory_service: MemoryService):
        self.provider = provider
        self.prompt_builder = prompt_builder
        self.memory_service = memory_service
        
    async def chat(self, conversation_id: str, user_message: str):
        # 1. Load history
        history = self.memory_service.load_history(conversation_id)
        
        # 2. Build the full prompt (system + history + new user message)
        messages = self.prompt_builder.build(history, user_message)
        
        # 3. Save the new user message to memory
        self.memory_service.save_user_message(conversation_id, user_message)

        # 4. Stream response from provider
        stream = self.provider.chat(messages)
        
        # 5. Intercept the stream to accumulate and save the assistant's message
        async def stream_and_save():
            full_response = ""
            async for chunk in stream:
                full_response += chunk
                yield chunk
            
            self.memory_service.save_assistant_message(conversation_id, full_response)

        return stream_and_save()
