from app.tools.base import BaseTool

class CalculatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Evaluates mathematical expressions."
        
    @property
    def parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate, e.g., '2 + 2 * 3'"
                }
            },
            "required": ["expression"]
        }

    async def execute(self, expression: str) -> str:
        try:
            # Using eval cautiously for basic math. In a real production environment, 
            # consider using a dedicated math parser for security.
            result = eval(expression, {"__builtins__": None}, {})
            return str(result)
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"
