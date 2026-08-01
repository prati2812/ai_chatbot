from app.prompts.general import SYSTEM_PROMPT

class PromptBuilder:
    def build(self, user_message: str) -> list[dict]:
        return [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
