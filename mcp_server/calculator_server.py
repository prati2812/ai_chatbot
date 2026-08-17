from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calculator")

@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluates mathematical expressions."""
    # Using eval cautiously for basic math.
    return str(eval(expression, {"__builtins__": None}, {}))

if __name__ == "__main__":
    mcp.run()
