from app.providers.base import AIProvider
from app.builders.prompt_builder import PromptBuilder

class ChatService:
    def __init__(self, provider: AIProvider, prompt_builder: PromptBuilder):
        self.provider = provider
        self.prompt_builder = prompt_builder
        
    async def chat(self, user_message: str):
        # Wrap the user message using the PromptBuilder
        messages = self.prompt_builder.build(user_message)

        # Pass the formatted messages to the provider
        return self.provider.chat(messages)
