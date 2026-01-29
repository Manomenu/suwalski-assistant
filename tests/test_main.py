from unittest.mock import patch
from suwalski_assistant.main import main

def test_main_execution():
    """
    Test that the main function calls the async entry point.
    """
    with patch('suwalski_assistant.main.asyncio.run') as mock_run:
        main()
        mock_run.assert_called_once()