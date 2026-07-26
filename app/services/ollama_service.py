# Ollama integration service
import json
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
            "stream" : True
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST", 
                f"{settings.ollama_base_url}/api/chat",
                json=payload
            ) as response:
                response.raise_for_status()
                async for chunk in response.aiter_lines():
                    if chunk:
                        data = json.loads(chunk)
                        if "message" in data and "content" in data["message"]:
                            yield data["message"]["content"]