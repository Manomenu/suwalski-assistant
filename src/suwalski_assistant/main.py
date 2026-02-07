from suwalski_assistant.entry_agent import entry_agent
from suwalski_assistant.discord_bot import run_discord_bot
import logging

def main():
    """
    Main entry point for the application.
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )


    run_discord_bot(entry_agent)

if __name__ == "__main__":
    main()