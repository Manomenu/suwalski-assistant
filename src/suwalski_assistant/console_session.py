import asyncio
import logging
import uuid
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

async def run_console_session(agent):
    """
    Initializes the runner with the provided agent and starts a console interaction loop.
    """
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        session_service=session_service,
        app_name="SuwalskiConsoleSession"
    )
    
    user_id = "console_user"
    session_id = str(uuid.uuid4())
    
    print(f"--- Suwalski Assistant Console (Agent: {agent.name}) ---")
    print("Type 'exit' or 'quit' to stop.")
    
    # Ensure session exists
    await session_service.create_session(app_name=runner.app_name, user_id=user_id, session_id=session_id)

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
            
            if not user_input:
                continue

            user_msg = types.Content(role='user', parts=[types.Part(text=user_input)])
            
            response_text = ""
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=user_msg
            ):
                if event.author != user_id and event.content:
                    response_text = ""
                    for part in event.content.parts:
                        if part.text:
                            response_text += part.text
            
            if response_text:
                print(f"Assistant: {response_text}")
            else:
                print("Assistant: (No response)")

        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Error in console session: {e}")
            print(f"An error occurred: {e}")

def run_console_bot(agent):
    asyncio.run(run_console_session(agent))
