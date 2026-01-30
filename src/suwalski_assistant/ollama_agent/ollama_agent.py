import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import logging

logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)

# Configuration
# Ensure you have pulled the model: `ollama pull qwen2:0.5b`
model_name = os.getenv("OLLAMA_MODEL", "ollama/qwen2:0.5b")

# Initialize the model wrapper
# LiteLLM handles the connection to Ollama
ollama_model = LiteLlm(model=model_name)

# Define the root agent
# This object is exported and used by the runner
root_agent = Agent(
    name="OllamaAssistant",
    model=ollama_model,
    instruction="You are a helpful AI assistant running locally via Ollama. Keep your responses concise."
)
