from app.providers.base import AIProvider

class GeminiProvider(AIProvider):
    async def chat(self, messages: list[dict]):
        # Dummy implementation
        yield "Gemini response"
