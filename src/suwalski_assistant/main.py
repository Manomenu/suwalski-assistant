from suwalski_assistant.entry_agent import entry_agent
from suwalski_assistant.discord_bot import run_discord_bot
from suwalski_assistant.console_session import run_console_bot
from suwalski_assistant.settings import settings
import logging

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )

def main():
    """
    Main entry point for the application.
    """

    if settings.input_mode == "discord":
        run_discord_bot(entry_agent)
    else:
        run_console_bot(entry_agent)

if __name__ == "__main__":
    main()