import os
import subprocess
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

def configure_environment():
    """
    Checks for LLM_ENV and runs env-configure.sh to sync .env file.
    """
    llm_env = os.getenv("LLM_ENV")
    if llm_env:
        script_path = os.path.join("scripts", "env-configure.sh")
        if os.path.exists(script_path):
            try:
                # Use bash to run the script, common for .sh files on Windows/Linux
                subprocess.run(["bash", script_path, llm_env], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"Warning: Failed to execute {script_path}: {e}")
        else:
            print(f"Warning: Configuration script not found at {script_path}")

# Run environment configuration before Pydantic loads settings
configure_environment()

class Settings(BaseSettings):
    input_mode: str = "console"
    discord_token: Optional[str] = None
    discord_channel_id: Optional[str] = None
    
    ollama_model: str = "ollama/qwen2:0.5b"
    ollama_api_key: str = "ollama"
    ollama_api_base: str = "http://localhost:11434"
    llm_env: str = "default"

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
