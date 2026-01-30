import asyncio
from google.adk.runners import InMemoryRunner
from google.genai import types
from suwalski_assistant.ollama_agent import ollama_agent

async def async_main():
    """
    Connects to a local Ollama instance using Google ADK and LiteLLM,
    and prints a response to 'hello'.
    """
    print(f"Connecting to Ollama using agent: {ollama_agent.name}...")
    
    try:
        # Create the runner with the imported agent
        runner = InMemoryRunner(agent=ollama_agent)

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
            if event.author == ollama_agent.name and event.content:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agent: {part.text}")

    except Exception as e:
        print(f"\nError: Could not connect to Ollama or generate response.")
        print(f"Details: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Docker is running and the Ollama container is up: `docker-compose up -d`")
        print(f"2. Ensure you have the model pulled: `docker exec -it <container_id> ollama pull <model_name>`")

def main():
    """
    Synchronous entry point for the application.
    """
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
