# Core configuration
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    default_provider: str = "ollama"
    use_native_tools: bool = False
    ollama_base_url: str
    ollama_model: str
    max_history_messages: int = 20

    class Config:
        env_file = ".env"

settings = Settings()        