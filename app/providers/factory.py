from app.providers.base import AIProvider
from app.providers.ollama_provider import OllamaProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider

class ProviderFactory:
    @staticmethod
    def get_provider(provider_name: str) -> AIProvider:
        name = provider_name.lower()
        if name == "ollama":
            return OllamaProvider()
        elif name == "openai":
            return OpenAIProvider()
        elif name == "gemini":
            return GeminiProvider()
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
