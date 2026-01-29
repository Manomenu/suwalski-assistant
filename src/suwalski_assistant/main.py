import asyncio
import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

async def async_main():
    """
    Connects to a local Ollama instance using Google ADK and LiteLLM,
    and prints a response to 'hello'.
    """
    # Configuration
    # Ensure you have pulled the model: `ollama pull qwen2:0.5b`
    model_name = os.getenv("OLLAMA_MODEL", "ollama/qwen2:0.5b")
    
    print(f"Connecting to Ollama using model: {model_name}...")
    
    try:
        # Initialize the model wrapper
        # LiteLLM handles the connection to Ollama
        ollama_model = LiteLlm(model=model_name)

        # Create the agent
        agent = Agent(
            name="OllamaAssistant",
            model=ollama_model,
            instruction="You are a helpful AI assistant running locally via Ollama. Keep your responses concise."
        )

        # Generate a response
        query = "hello"
        print(f"User: {query}")
        
        # Note: The exact method might vary based on ADK version, 
        # but generate_response is standard.
        response = await agent.generate_response(query)
        
        print(f"Agent: {response.text}")

    except Exception as e:
        print(f"\nError: Could not connect to Ollama or generate response.")
        print(f"Details: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Docker is running and the Ollama container is up: `docker-compose up -d`")
        print(f"2. Ensure you have the model pulled: `docker exec -it <container_id> ollama pull {model_name.replace('ollama/', '')}`")

def main():
    """
    Synchronous entry point for the application.
    """
    asyncio.run(async_main())

if __name__ == "__main__":
    main()