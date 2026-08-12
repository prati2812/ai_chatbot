import json
import httpx

from app.core.config import settings
from app.providers.base import AIProvider
from app.schemas.events import StreamEvent
import asyncio

class OllamaProvider(AIProvider):

    async def chat(self, messages: list[dict], tools: list[dict] = None):
        payload = {
            "model": settings.ollama_model,
            "messages": messages,
            "stream": settings.use_native_tools # Stream only if native tools are enabled
        }
        
        if tools and settings.use_native_tools:
            payload["tools"] = tools

        async with httpx.AsyncClient(timeout=60.0) as client:
            if not settings.use_native_tools:
                # ReAct Fallback (Non-Streaming)
                response = await client.post(
                    f"{settings.ollama_base_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                content = data.get("message", {}).get("content", "")
                yield StreamEvent(type="text", content=content)
                return

            # Native Tools (Streaming)
            async with client.stream(
                "POST", 
                f"{settings.ollama_base_url}/api/chat",
                json=payload
            ) as response:
                response.raise_for_status()
                
                async for chunk in response.aiter_lines():
                    if not chunk:
                        continue
                        
                    data = json.loads(chunk)
                    msg = data.get("message", {})
                    
                    if "tool_calls" in msg and msg["tool_calls"]:
                        for tool_call in msg["tool_calls"]:
                            yield StreamEvent(type="tool_call", tool_call=tool_call)
                            
                    elif "content" in msg and msg["content"]:
                        yield StreamEvent(type="text", content=msg["content"])
