from app.providers.base import AIProvider
from app.builders.prompt_builder import PromptBuilder
from app.services.memory_service import MemoryService
from app.services.context_manager import ContextManager
from app.services.token_manager import TokenManager
from app.parsers.output_parser import OutputParser
from app.executors.tool_executor import ToolExecutor
from app.tools.factory import ToolFactory

class ChatService:
    def __init__(self, provider: AIProvider, prompt_builder: PromptBuilder, memory_service: MemoryService, context_manager: ContextManager, token_manager: TokenManager, output_parser: OutputParser, tool_executor: ToolExecutor):
        self.provider = provider
        self.prompt_builder = prompt_builder
        self.memory_service = memory_service
        self.context_manager = context_manager
        self.token_manager = token_manager
        self.output_parser = output_parser
        self.tool_executor = tool_executor
        
    async def chat(self, conversation_id: str, user_message: str):
        # 1. Save the new user message to memory FIRST
        self.memory_service.save_user_message(conversation_id, user_message)

        # 2. Load history (which now includes the user's message)
        history = self.memory_service.load_history(conversation_id)

        selected_history = self.context_manager.get_context(history)
        
        # 3. Build the full prompt (system + history)
        messages = self.prompt_builder.build(selected_history)

        # 4. Prepare messages to fit token limits
        messages = self.token_manager.prepare(messages)

        tools = ToolFactory.get_all_schemas()
        max_iterations = 5

        for _ in range(max_iterations):

            response = await self.provider.chat(
                messages=messages,
                tools=tools
            )

            message = response["message"]
            tool_calls = message.get("tool_calls", [])

            # No tool requested
            if not tool_calls:
                final_answer = message.get("content", "")
                
                self.memory_service.save_assistant_message(
                    conversation_id,
                    final_answer
                )

                return final_answer

            # Model requested one or more tools
            messages.append(message)

            for tool_call in tool_calls:
                function = tool_call["function"]
                tool_name = function["name"]
                arguments = function["arguments"]

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

        return "Maximum tool-call iterations reached."
