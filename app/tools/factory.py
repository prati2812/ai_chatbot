from typing import Dict, Type
import sys
from app.tools.base import BaseTool
# from app.tools.calculator import CalculatorTool # (Local calculator disabled in favor of MCP)
from app.mcp.client import MCPClient
from app.tools.mcp_proxy_tool import MCPProxyTool

class ToolFactory:
    _local_tools: Dict[str, Type[BaseTool]] = {
        # "calculator": CalculatorTool, # Disabled, running via MCP instead!
    }
    
    _mcp_client: MCPClient | None = None
    _mcp_tools: Dict[str, BaseTool] = {}

    @classmethod
    async def initialize(cls):
        """Initializes the MCP client and fetches tools."""
        if cls._mcp_client is not None:
            return

        cls._mcp_client = MCPClient(command=sys.executable, args=["mcp_server/calculator_server.py"])
        await cls._mcp_client.connect()
        
        mcp_tools = await cls._mcp_client.list_tools()
        for t in mcp_tools:
            proxy_tool = MCPProxyTool(
                mcp_client=cls._mcp_client,
                name=t.name,
                description=t.description or "",
                parameters_schema=t.inputSchema
            )
            cls._mcp_tools[t.name] = proxy_tool

    @classmethod
    def get_tool(cls, name: str) -> BaseTool:
        if name in cls._mcp_tools:
            return cls._mcp_tools[name]
            
        tool_class = cls._local_tools.get(name)
        if not tool_class:
            raise ValueError(f"Tool '{name}' not found.")
        return tool_class()
        
    @classmethod
    async def get_all_schemas(cls) -> list[dict]:
        """Returns the JSON schema for all available tools to pass to the LLM."""
        await cls.initialize()
        
        schemas = []
        for name, tool_class in cls._local_tools.items():
            tool = tool_class()
            schemas.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters_schema
                }
            })
            
        for name, tool in cls._mcp_tools.items():
            schemas.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters_schema
                }
            })
            
        return schemas
