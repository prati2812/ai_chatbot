# Core configuration
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    default_provider: str = "ollama"
    ollama_base_url: str
    ollama_model: str

    class Config:
        env_file = ".env"

settings = Settings()        