import logging
import litellm
from google.adk.models.lite_llm import LiteLlm
from suwalski_assistant.settings import settings

logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)
litellm.telemetry = False

_original_acompletion = litellm.acompletion

async def patched_acompletion(*args, **kwargs):
    if "messages" in kwargs:
        for message in kwargs["messages"]:
            if "content" not in message or message["content"] is None:
                message["content"] = ""
    return await _original_acompletion(*args, **kwargs)

litellm.acompletion = patched_acompletion

base_model = LiteLlm(
    model=settings.base_model, 
    api_key=settings.base_api_key, 
    api_base=settings.base_api_base.rstrip("/")
)

vision_model = LiteLlm(
    model=settings.vision_model, 
    api_key=settings.vision_api_key, 
    api_base=settings.vision_api_base.rstrip("/")
)