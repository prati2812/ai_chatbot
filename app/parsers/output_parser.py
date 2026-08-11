import re
import json

class OutputParser:
    def parse(self, raw_output: str) -> dict:
        """
        Parses the raw text output from the AI provider into structured data.
        """
        pattern = r"@@TOOL_CALL:\s*({.*?})\s*@@"
        match = re.search(pattern, raw_output, re.DOTALL)
        
        if match:
            try:
                tool_call_json = match.group(1)
                parsed_call = json.loads(tool_call_json)
                
                return {
                    "type": "tool_call",
                    "calls": [
                        {
                            "function": {
                                "name": parsed_call.get("name"),
                                "arguments": parsed_call.get("arguments", {})
                            }
                        }
                    ]
                }
            except json.JSONDecodeError:
                pass
                
        return {
            "type": "text",
            "content": raw_output
        }
