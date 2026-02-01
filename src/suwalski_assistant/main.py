from suwalski_assistant.ollama_agent import ollama_agent
from suwalski_assistant.discord_bot import run_discord_bot

def main():
    """
    Main entry point for the application.
    """

    run_discord_bot(ollama_agent)

if __name__ == "__main__":
    main()