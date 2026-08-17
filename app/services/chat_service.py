from app.providers.base import AIProvider
from app.builders.prompt_builder import PromptBuilder
from app.services.memory_service import MemoryService
from app.services.context_manager import ContextManager
from app.services.token_manager import TokenManager
from app.parsers.output_parser import OutputParser
from app.executors.tool_executor import ToolExecutor
from app.tools.factory import ToolFactory
from app.core.config import settings
from typing import AsyncGenerator
import json
from app.events.stream_event import StreamEvent
class ChatService:
    def __init__(self, provider: AIProvider, prompt_builder: PromptBuilder, memory_service: MemoryService, context_manager: ContextManager, token_manager: TokenManager, output_parser: OutputParser, tool_executor: ToolExecutor):
        self.provider = provider
        self.prompt_builder = prompt_builder
        self.memory_service = memory_service
        self.context_manager = context_manager
        self.token_manager = token_manager
        self.output_parser = output_parser
        self.tool_executor = tool_executor
        
    async def chat(self, conversation_id: str, user_message: str) -> AsyncGenerator[StreamEvent, None]:
        # 1. Save the new user message to memory FIRST
        self.memory_service.save_user_message(conversation_id, user_message)

        # 2. Load history (which now includes the user's message)
        history = self.memory_service.load_history(conversation_id)

        selected_history = self.context_manager.get_context(history)
        
        tools = await ToolFactory.get_all_schemas()

        # 3. Build the full prompt (system + history)
        messages = self.prompt_builder.build(selected_history, tools=tools)

        # 4. Prepare messages to fit token limits
        messages = self.token_manager.prepare(messages)

        max_iterations = 5

        for _ in range(max_iterations):

            tool_calls = []
            full_text = ""

            events = self.provider.chat(
                messages=messages,
                tools=tools
            )

            if not settings.use_native_tools:
                # ReAct fallback path
                async for event in events:
                    if event.type == "text":
                        raw_content = event.content or ""
                        parsed = self.output_parser.parse(raw_content)
                        
                        if parsed["type"] == "tool_call":
                            tool_calls.extend([c["function"] for c in parsed["calls"]])
                        else:
                            full_text += parsed["content"]
                            yield StreamEvent(type="text", data=parsed["content"])
            else:
                # Native streaming path
                async for event in events:
                    if event.type == "text":
                        if event.content:
                            full_text += event.content
                            yield StreamEvent(type="text", data=event.content)
                    elif event.type == "tool_call":
                        tool_calls.append(event.tool_call["function"])

            # No tool requested
            if not tool_calls:
                self.memory_service.save_assistant_message(
                    conversation_id,
                    full_text
                )
                return

            # Model requested one or more tools
            messages.append({
                "role": "assistant",
                "content": full_text,
                "tool_calls": [{"type": "function", "function": tc} for tc in tool_calls]
            })

            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                arguments = tool_call["arguments"]
                
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        pass

                # Ensure we await the async tool executor
                result = await self.tool_executor.execute(
                    tool_name,
                    arguments
                )

                messages.append({
                    "role": "tool",
                    "content": result,
                    "name": tool_name
                })

        yield StreamEvent(type="done", data="Maximum tool-call iterations reached.")
