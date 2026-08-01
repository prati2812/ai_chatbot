from app.providers.base import AIProvider

class ChatService:
    def __init__(self, provider: AIProvider):
        # We inject the provider here. 
        # This way, ChatService doesn't care if it's Ollama, OpenAI, etc.
        self.provider = provider
        
    async def chat(self, user_message: list[dict]):
        # TODO: Later, you can use your prompt_builder here to wrap the user_message
        # formatted_message = prompt_builder.build("general", user_message)
        
        # For now, we just pass the message directly to the provider
        messages = [
            {
                "role": "user",
                "content": user_message
            }
        ]

        return self.provider.chat(messages)

