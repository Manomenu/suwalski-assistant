import asyncio
import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.genai import types

async def async_main():
    """
    Connects to a local Ollama instance using Google ADK and LiteLLM,
    and prints a response to 'hello'.
    """
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

        # Create the runner
        runner = InMemoryRunner(agent=agent)

        # Create session explicitly
        await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id="local_user",
            session_id="local_session"
        )

        # Create user message
        user_msg = types.Content(parts=[types.Part(text="hello")])
        print(f"User: hello")

        # Run the agent
        async for event in runner.run_async(
            user_id="local_user",
            session_id="local_session",
            new_message=user_msg
        ):
            # Print agent responses
            if event.author == "OllamaAssistant" and event.content:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agent: {part.text}")

    except Exception as e:
        print(f"\nError: Could not connect to Ollama or generate response.")
        print(f"Details: {e}")

def main():
    """
    Synchronous entry point for the application.
    """
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
