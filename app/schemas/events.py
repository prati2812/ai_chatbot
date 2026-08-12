from pydantic import BaseModel
from typing import Optional

class StreamEvent(BaseModel):
    type: str # "text", "tool_call"
    content: Optional[str] = None
    tool_call: Optional[dict] = None
