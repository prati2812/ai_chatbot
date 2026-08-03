from app.prompts.general import SYSTEM_PROMPT

class PromptBuilder:
    def build(self, history: list[dict]) -> list[dict]:
        return [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            *history
        ]
