class TokenManager:

    def __init__(
        self,
        max_tokens: int = 7000
    ):
        self.max_tokens = max_tokens

    def count_tokens(
        self,
        messages: list[dict]
    ) -> int:

        total = 0

        for message in messages:

            total += len(
                message["content"].split()
            )

        return total

    def fits_context(
        self,
        messages: list[dict]
    ) -> bool:

        return (
            self.count_tokens(messages)
            <= self.max_tokens
        )

    def prepare(
        self,
        messages: list[dict]
    ) -> list[dict]:

        if self.count_tokens(messages) <= self.max_tokens:
            return messages

        return self._trim(messages)

    def _trim(
        self,
        messages: list[dict]
    ) -> list[dict]:
        
        # Keep trimming the oldest message (index 1) until it fits context.
        # We preserve index 0 (system prompt) and ensure we don't trim the latest user message.
        while self.count_tokens(messages) > self.max_tokens and len(messages) > 2:
            messages.pop(1)
            
        return messages