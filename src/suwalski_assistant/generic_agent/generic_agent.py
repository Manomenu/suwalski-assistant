from google.adk.agents import LlmAgent
from suwalski_assistant.llm_models import ollama_model
from suwalski_assistant.constants import *

root_agent = LlmAgent(
    name=AGENT_NAMES.GENERIC_AGENT,
    description="Gives helpful answers as discord assistant.",
    instruction="You are a helpful assistant for user in discord channel. Answer when asked.",
    model=ollama_model
)