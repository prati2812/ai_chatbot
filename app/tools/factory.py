from typing import Dict, Type
from app.tools.base import BaseTool
from app.tools.calculator import CalculatorTool

class ToolFactory:
    _tools: Dict[str, Type[BaseTool]] = {
        "calculator": CalculatorTool,
    }

    @classmethod
    def get_tool(cls, name: str) -> BaseTool:
        tool_class = cls._tools.get(name)
        if not tool_class:
            raise ValueError(f"Tool '{name}' not found.")
        return tool_class()
        
    @classmethod
    def get_all_schemas(cls) -> list[dict]:
        """Returns the JSON schema for all available tools to pass to the LLM."""
        schemas = []
        for name, tool_class in cls._tools.items():
            tool = tool_class()
            schemas.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters_schema
                }
            })
        return schemas
