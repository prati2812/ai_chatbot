class ContextManager:

    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages

    def get_context(
        self,
        history: list[dict]
    ) -> list[dict]:

        return history[-self.max_messages:]