from typing import Optional, Literal
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from pydantic import BaseModel, Field
from suwalski_assistant.generic_agent import generic_agent
from suwalski_assistant.llm_models import ollama_model
from suwalski_assistant.constants import AGENTIC_OUTPUT_KEYS as aok
from suwalski_assistant.tools import *
from suwalski_assistant.constants import AGENT_NAMES as an


class ImageTypeOutput(BaseModel):
    image_type: Literal["NOTES", "OTHER"] = Field(description="'NOTES' if provided image contains handwritten note, 'OTHER' otherwise.")


def handle_handwritten_notes(callback_context: CallbackContext) -> Optional[types.Content]:
    state_data = callback_context.state[aok.DETECTED_IMAGE_TYPE]
    state = ImageTypeOutput(**state_data) if isinstance(state_data, dict) else state_data
    image_type = state.image_type.strip().upper()

    if image_type == "NOTES":
        return content_from_text("Message has been handled, handwritten notes saved to Obsidian Vault.")
    return content_from_text("Image does not contain handwritten note. Call other agent to answer message.")


handwritten_notes_classifier_agent = LlmAgent(
    name=an.HANDWRITTEN_NOTES_CLASSIFIER_AGENT,
    model=ollama_model,
    instruction="Decide whether provided image contains handwritten notes. NOTES - image contains handwritten notes, OTHER - image does not contains handwritten notes.",
    output_schema=ImageTypeOutput,
    output_key=aok.DETECTED_IMAGE_TYPE,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    
)

root_agent = SequentialAgent(
    name=an.HANDWRITTEN_NOTES_AGENT,
    description="""
        Identifies whether provided image is an handwritten note and saves it as markdown in Obsidian if possible. 
        Can be called if there is an image and no text in the message.
    """,
    sub_agents=[handwritten_notes_classifier_agent],
    after_agent_callback=handle_handwritten_notes
)

