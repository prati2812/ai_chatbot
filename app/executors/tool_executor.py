import jsonschema
import asyncio
import json
from app.tools.factory import ToolFactory

class ToolExecutor:
    def __init__(self, allowed_tools: list[str] = None, timeout_seconds: float = 30.0, max_executions: int = 50):
        # If None, all tools registered in the factory are allowed.
        self.allowed_tools = allowed_tools
        self.timeout_seconds = timeout_seconds
        self.max_executions = max_executions
        self.execution_count = 0

    def _normalize_result(self, success: bool, data: any = None, error_type: str = None, error_message: str = None) -> str:
        """Step 8: Normalize result into a standard JSON format for the LLM."""
        if success:
            payload = {
                "success": True,
                "result": data
            }
        else:
            payload = {
                "success": False,
                "error": {
                    "type": error_type,
                    "message": error_message
                }
            }
        return json.dumps(payload)

    async def execute(self, tool_name: str, arguments: dict) -> str:
        """
        Orchestrates the execution of a tool requested by the AI.
        """
        # Step 5: Apply execution limits (placed early to prevent abuse)
        if self.execution_count >= self.max_executions:
            return self._normalize_result(False, error_type="RATE_LIMIT", error_message="Maximum tool execution limit reached for this session.")
        self.execution_count += 1

        # Step 1: Resolve tool
        try:
            tool = ToolFactory.get_tool(tool_name)
        except ValueError:
            return self._normalize_result(False, error_type="NOT_FOUND", error_message=f"Tool '{tool_name}' does not exist.")

        # Step 2: Check authorization
        if self.allowed_tools is not None and tool_name not in self.allowed_tools:
            return self._normalize_result(False, error_type="UNAUTHORIZED", error_message=f"Tool '{tool_name}' is not allowed in this context.")

        # Step 3: Validate arguments
        try:
            jsonschema.validate(instance=arguments, schema=tool.parameters_schema)
        except jsonschema.exceptions.ValidationError as e:
            return self._normalize_result(False, error_type="VALIDATION_ERROR", error_message=f"Invalid arguments provided for '{tool_name}'. Error: {e.message}")

        # Step 4 & 6: Apply timeout and Execute
        try:
            # Await execution wrapped in asyncio.wait_for to apply a strict timeout
            result = await asyncio.wait_for(tool.execute(**arguments), timeout=self.timeout_seconds)
            
            # Step 7: Validate result (ensure it's serializable or a string)
            if not isinstance(result, (str, int, float, bool, dict, list)):
                result = str(result)
                
            # Step 9: Return normalized success result
            return self._normalize_result(True, data=result)
            
        except asyncio.TimeoutError:
            return self._normalize_result(False, error_type="TIMEOUT", error_message=f"The '{tool_name}' tool timed out after {self.timeout_seconds} seconds.")
        except Exception as e:
            return self._normalize_result(False, error_type="EXECUTION_ERROR", error_message=f"Tool '{tool_name}' failed during execution: {str(e)}")
