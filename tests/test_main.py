from unittest.mock import patch
from suwalski_assistant.main import main

def test_main_execution():
    """
    Test that the main function calls the discord bot runner.
    """
    with patch('suwalski_assistant.main.run_discord_bot') as mock_run_discord_bot:
        main()
        mock_run_discord_bot.assert_called_once()