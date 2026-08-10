import json
from app.prompts.general import SYSTEM_PROMPT
from app.core.config import settings

class PromptBuilder:
    def build(self, history: list[dict], tools: list[dict] = None) -> list[dict]:
        system_content = SYSTEM_PROMPT
        
        if tools and not settings.use_native_tools:
            tool_instructions = (
                "\n\nYou have access to the following tools:\n"
                f"{json.dumps(tools, indent=2)}\n\n"
                "To use a tool, you MUST respond ONLY with the exact following JSON format enclosed in @@TOOL_CALL: and @@ tags:\n"
                "@@TOOL_CALL: {\"name\": \"tool_name\", \"arguments\": {\"arg1\": \"value1\"}}@@\n"
                "If you want to answer the user directly without using a tool, simply write your response without any tags."
            )
            system_content += tool_instructions

        return [
            {
                "role": "system",
                "content": system_content
            },
            *history
        ]
