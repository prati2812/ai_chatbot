from app.prompts.general import SYSTEM_PROMPT

class PromptBuilder:
    def build(self, history: list[dict], user_message: str) -> list[dict]:
        return [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            *history,
            {
                "role": "user",
                "content": user_message
            }
        ]
