import os
import logging
from google.adk.models.lite_llm import LiteLlm

logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)

# Configuration
# Ensure you have pulled the model: `ollama pull qwen2:0.5b`
model_name = os.getenv("OLLAMA_MODEL", "ollama/qwen2:0.5b")
api_key = os.getenv("OLLAMA_API_KEY", "ollama")
api_base = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

# Initialize the model wrapper
# LiteLLM handles the connection to Ollama
# ollama_model = LiteLlm(model=model_name, api_key=api_key, api_base=api_base)
ollama_model = LiteLlm(model=model_name)