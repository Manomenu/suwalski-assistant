import logging
from google.adk.models.lite_llm import LiteLlm
from suwalski_assistant.settings import settings

logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)
logging.log(logging.INFO, f"LLM_ENV: {settings.llm_env}")

ollama_model = LiteLlm(
    model=settings.ollama_model, 
    api_key=settings.ollama_api_key, 
    api_base=settings.ollama_api_base
)