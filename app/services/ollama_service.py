# Ollama integration service
import httpx

from app.core.config import settings

class OllamaService:

    async def chat(self, message: str):
        payload = {
            "model": settings.ollama_model,
            "messages": [
                {
                    "role" : "user",
                    "content" : message
                }
            ],
            "stream" : False 
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()

            return response.json()