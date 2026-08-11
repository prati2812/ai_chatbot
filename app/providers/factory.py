from app.providers.base import AIProvider
from app.providers.ollama_provider import OllamaProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider

PROVIDERS = {
    "ollama": OllamaProvider,
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
}

class ProviderFactory:
    @staticmethod
    def get_provider(provider_name: str) -> AIProvider:
        name = provider_name.lower()
        provider_class = PROVIDERS.get(name)
        
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_name}")
            
        return provider_class()
