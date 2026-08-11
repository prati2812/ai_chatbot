class MemoryService:
    def __init__(self):
        self.chat_memory: dict[str, list[dict]] = {}
        
    def load_history(self, conversation_id: str) -> list[dict]:
        return self.chat_memory.get(conversation_id, [])
        
    def save_user_message(self, conversation_id: str, content: str):
        if conversation_id not in self.chat_memory:
            self.chat_memory[conversation_id] = []
        self.chat_memory[conversation_id].append({"role": "user", "content": content})
        
    def save_assistant_message(self, conversation_id: str, content: str):
        if conversation_id not in self.chat_memory:
            self.chat_memory[conversation_id] = []
        self.chat_memory[conversation_id].append({"role": "assistant", "content": content})
