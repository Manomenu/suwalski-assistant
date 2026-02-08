import pytest
from unittest.mock import MagicMock
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from suwalski_assistant.handwritten_notes_agent.handwritten_notes_agent import try_save_handwritten_note, ImageTypeOutput
from suwalski_assistant.constants import AGENTIC_OUTPUT_KEYS as aok

def test_handle_handwritten_notes_is_note():
    # Setup
    callback_context = MagicMock(spec=CallbackContext)
    callback_context.state = {
        aok.DETECTED_IMAGE_TYPE: ImageTypeOutput(image_type="NOTES"),
        aok.NOTE_MARKDOWN_DATA: {
            "markdown_title": "Test Note",
            "markdown_content": "This is a test note."
        }
    }
    
    # Execute
    result = try_save_handwritten_note(callback_context)

    # Verify
    assert result is not None
    assert "handwritten notes saved to Obsidian Vault" in result.parts[0].text

def test_handle_handwritten_notes_is_other():
    # Setup
    callback_context = MagicMock(spec=CallbackContext)
    callback_context.state = {
        aok.DETECTED_IMAGE_TYPE: ImageTypeOutput(image_type="OTHER")
    }
    
    # Execute
    result = try_save_handwritten_note(callback_context)

    # Verify
    assert result is not None
    assert "Image does not contain handwritten note" in result.parts[0].text