import logging
from google.adk.models.lite_llm import LiteLlm
from suwalski_assistant.settings import settings
import litellm

logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)
logging.info(f"LLM_ENV: {settings.llm_env}")

litellm.telemetry = False

class FixedLiteLlm(LiteLlm):
    async def acompletion(self, *args, **kwargs):
        if "messages" in kwargs:
            for message in kwargs["messages"]:
                if "content" not in message or message["content"] is None:
                    message["content"] = ""
        
        return await super().acompletion(*args, **kwargs)

ollama_model = FixedLiteLlm(
    model=settings.ollama_model, 
    api_key=settings.ollama_api_key, 
    api_base=settings.ollama_api_base
)