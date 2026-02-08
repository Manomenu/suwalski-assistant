from suwalski_assistant.entry_agent import entry_agent
from suwalski_assistant.input_interface import run_discord_bot, run_console_bot
from suwalski_assistant.settings import settings
from suwalski_assistant.services.logging_config import setup_logging
def main():
    """
    Main entry point for the application.
    """
    setup_logging()

    if settings.input_mode == "discord":
        run_discord_bot(entry_agent)
    else:
        run_console_bot(entry_agent)

if __name__ == "__main__":
    main()