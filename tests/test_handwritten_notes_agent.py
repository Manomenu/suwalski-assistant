
import pytest
from unittest.mock import MagicMock
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from suwalski_assistant.handwritten_notes_agent.handwritten_notes_agent import handwritten_notes_after_callback

def test_handwritten_notes_after_callback_is_note():
    # Setup
    callback_context = MagicMock(spec=CallbackContext)
    
    # Mock LLM Response saying "NOTES"
    llm_response = LlmResponse(
        content=types.Content(parts=[types.Part(text="NOTES")])
    )

    # Execute
    result = handwritten_notes_after_callback(callback_context, llm_response)

    # Verify
    assert result is not None
    assert result.content.parts[0].text == "Notes saved to Obsidian Vault"

def test_handwritten_notes_after_callback_is_other():
    # Setup
    callback_context = MagicMock(spec=CallbackContext)
    
    # Mock LLM Response saying "OTHER"
    llm_response = LlmResponse(
        content=types.Content(parts=[types.Part(text="OTHER")])
    )

    # Execute
    result = handwritten_notes_after_callback(callback_context, llm_response)

    # Verify
    assert result is None
