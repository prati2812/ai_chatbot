from app.tools.factory import ToolFactory

class ToolExecutor:
    async def execute(self, tool_name: str, arguments: dict) -> str:
        """
        Orchestrates the execution of a tool requested by the AI.
        """
        try:
            tool = ToolFactory.get_tool(tool_name)
            result = await tool.execute(**arguments)
            return result
        except Exception as e:
            return f"Tool execution failed: {str(e)}"
