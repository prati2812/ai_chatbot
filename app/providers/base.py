from abc import ABC, abstractmethod

class AIProvider(ABC):
    
    @abstractmethod
    async def chat(self, messages: list[dict], tools: list[dict] = None):
        pass