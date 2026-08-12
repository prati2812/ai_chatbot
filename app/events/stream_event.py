from dataclasses import dataclass
from typing import Any

@dataclass
class StreamEvent:
    type: str
    data: Any
