from abc import ABC, abstractmethod

class AIProvider(ABC):
    
    @abstractmethod
    async def chat(self, messages):
        pass