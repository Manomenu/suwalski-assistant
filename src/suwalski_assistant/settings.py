from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings managed by Pydantic.
    Loads from .env.
    """
    discord_token: str
    discord_channel_id: Optional[str] = None
    
    # Ollama / LLM Settings
    ollama_model: str = "ollama/qwen2:0.5b"
    ollama_api_key: str = "ollama"
    ollama_api_base: str = "http://localhost:11434"

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=False
    )

try:
    settings = Settings()
except Exception as e:
    print(f"Failed to load settings: {e}")
    raise
