import json
import httpx

from app.core.config import settings
from app.providers.base import AIProvider  # Import your base class

class OllamaProvider(AIProvider):

    async def chat(self, messages: list[dict], tools: list[dict] = None):
        payload = {
            "model": settings.ollama_model,
            "messages": messages,
            "stream" : False
        }
        
        if tools and settings.use_native_tools:
            payload["tools"] = tools

        async with httpx.AsyncClient(timeout=60.0) as client:
            # async with client.stream(
            #     "POST", 
            #     f"{settings.ollama_base_url}/api/chat",
            #     json=payload
            # ) as response:
            #     response.raise_for_status()
            #     return response.json()
            #     # async for chunk in response.aiter_lines():
            #     #     if chunk:
            #     #         data = json.loads(chunk)
            #             
            #     #         if "message" in data:
            #     #             msg = data["message"]
            #                 
            #     #             if "tool_calls" in msg and msg["tool_calls"]:
            #     #                 yield {"type": "tool_call", "calls": msg["tool_calls"]}
            #     #             elif "content" in msg and msg["content"]:
            #     #                 yield {"type": "text", "content": msg["content"]}

            response = await client.post(
                f"{settings.ollama_base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data
