from app.tools.base import BaseTool
from app.mcp.client import MCPClient

class MCPProxyTool(BaseTool):
    def __init__(self, mcp_client: MCPClient, name: str, description: str, parameters_schema: dict):
        self._name = name
        self._description = description
        self._parameters_schema = parameters_schema
        self.mcp_client = mcp_client

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def parameters_schema(self) -> dict:
        return self._parameters_schema

    async def execute(self, **kwargs) -> str:
        # Call the tool over MCP
        content = await self.mcp_client.call_tool(self._name, kwargs)
        
        # MCP responses are a list of TextContent/ImageContent.
        # We extract the text.
        result_texts = []
        for item in content:
            if getattr(item, "type", None) == "text":
                result_texts.append(item.text)
        
        return "\n".join(result_texts)
