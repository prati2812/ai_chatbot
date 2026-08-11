from app.providers.base import AIProvider

class OpenAIProvider(AIProvider):
    async def chat(self, messages: list[dict]):
        # Dummy implementation
        yield "OpenAI response"
