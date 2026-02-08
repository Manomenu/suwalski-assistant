import pytest
import logging
from unittest.mock import MagicMock, patch
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from suwalski_assistant.handwritten_notes_agent.handwritten_notes_agent import (
    try_save_handwritten_note, 
    try_default_user_response,
    verify_handwritten_note_provided,
    ImageTypeOutput
)
from suwalski_assistant.constants import AGENTIC_OUTPUT_KEYS as aok

@pytest.fixture
def mock_callback_context():
    """Fixture for creating a mock CallbackContext."""
    context = MagicMock(spec=CallbackContext)
    context.state = {}
    return context

class TestHandwrittenNotesCallbacks:
    """Group of tests for handwritten notes agent callbacks."""

    def test_verify_handwritten_note_provided_is_note(self, mock_callback_context):
        """Test that verification passes when image is a note."""
        mock_callback_context.state = {
            aok.DETECTED_IMAGE_TYPE: ImageTypeOutput(image_type="NOTES")
        }
        result = verify_handwritten_note_provided(mock_callback_context)
        assert result is None

    def test_verify_handwritten_note_provided_is_other(self, mock_callback_context):
        """Test that verification fails when image is not a note."""
        mock_callback_context.state = {
            aok.DETECTED_IMAGE_TYPE: ImageTypeOutput(image_type="OTHER")
        }
        result = verify_handwritten_note_provided(mock_callback_context)
        assert result is not None
        assert "Image is not a note" in result.parts[0].text

    @patch("suwalski_assistant.handwritten_notes_agent.handwritten_notes_agent.save_note")
    def test_try_save_handwritten_note_with_sanitization(self, mock_save_note, mock_callback_context):
        """Test saving a note with title sanitization (removing / and \\)."""
        mock_callback_context.state = {
            aok.NOTE_MARKDOWN_DATA: {
                "markdown_title": "Folder/Subfolder\\MyNote",
                "markdown_content": "Note content here."
            }
        }
        
        try_save_handwritten_note(mock_callback_context)
        
        # Verify that save_note was called with the sanitized title
        mock_save_note.assert_called_once_with("Folder_Subfolder_MyNote", "Note content here.")

    def test_try_default_user_response_is_note(self, mock_callback_context):
        """Test that a success message is returned for notes."""
        mock_callback_context.state = {
            aok.DETECTED_IMAGE_TYPE: ImageTypeOutput(image_type="NOTES"),
            aok.NOTE_MARKDOWN_DATA: {
                "markdown_title": "My Great Note",
                "markdown_content": "Content"
            }
        }
        
        result = try_default_user_response(mock_callback_context)
        assert result is not None
        assert "Handwritten notes saved to Obsidian Vault as 'My Great Note'" in result.parts[0].text

    def test_try_default_user_response_is_other(self, mock_callback_context):
        """Test that no default response is returned if it's not a note."""
        mock_callback_context.state = {
            aok.DETECTED_IMAGE_TYPE: ImageTypeOutput(image_type="OTHER")
        }
        
        result = try_default_user_response(mock_callback_context)
        assert result is None
