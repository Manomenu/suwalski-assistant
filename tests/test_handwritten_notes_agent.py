import pytest
from unittest.mock import MagicMock
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from suwalski_assistant.handwritten_notes_agent.handwritten_notes_agent import handle_handwritten_notes, ImageTypeOutput
from suwalski_assistant.constants import AGENTIC_OUTPUT_KEYS as aok

def test_handle_handwritten_notes_is_note():
    # Setup
    callback_context = MagicMock(spec=CallbackContext)
    callback_context.state = {
        aok.DETECTED_IMAGE_TYPE: ImageTypeOutput(image_type="NOTES")
    }
    
    # Execute
    result = handle_handwritten_notes(callback_context)

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
    result = handle_handwritten_notes(callback_context)

    # Verify
    assert result is not None
    assert "Image does not contain handwritten note" in result.parts[0].text