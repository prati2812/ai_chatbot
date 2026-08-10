import asyncio
import httpx
import json

async def test():
    payload = {
        "model": "llama3",
        "messages": [
            {"role": "user", "content": "What is 123 * 456?"}
        ],
        "stream": False,
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "Evaluates mathematical expressions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "The mathematical expression to evaluate"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            }
        ]
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post("http://127.0.0.1:11434/api/chat", json=payload)
            print("Status:", resp.status_code)
            print("Response:", resp.text)
        except Exception as e:
            print("Error:", e)

asyncio.run(test())
