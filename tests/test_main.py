from unittest.mock import patch
from suwalski_assistant.main import main
from suwalski_assistant.settings import settings

def test_main_execution_discord():
    """
    Test that the main function calls the discord bot runner when input_mode is discord.
    """
    with patch.object(settings, 'input_mode', 'discord'), \
         patch.object(settings, 'discord_token', 'fake-token'), \
         patch('suwalski_assistant.main.run_discord_bot') as mock_run_discord_bot:
        main()
        mock_run_discord_bot.assert_called_once()

def test_main_execution_console():
    """
    Test that the main function calls the console session runner when input_mode is console.
    """
    with patch.object(settings, 'input_mode', 'console'), \
         patch('suwalski_assistant.main.run_console_bot') as mock_start_console_session:
        main()
        mock_start_console_session.assert_called_once()