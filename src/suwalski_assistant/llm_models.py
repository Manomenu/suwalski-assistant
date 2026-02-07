import os
import logging
from google.adk.models.lite_llm import LiteLlm

logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)

model_name = os.getenv("OLLAMA_MODEL", "ollama/qwen2:0.5b")
api_key = os.getenv("OLLAMA_API_KEY", "ollama")
api_base = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

ollama_model = LiteLlm(model=model_name, api_key=api_key, api_base=api_base)