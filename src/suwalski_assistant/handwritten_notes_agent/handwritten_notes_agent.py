from typing import Optional
from google.adk.agents import LlmAgent, SequentialAgent, Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from pydantic import BaseModel, Field
from suwalski_assistant.llm_models import ollama_model
from suwalski_assistant.constants import AGENTIC_OUTPUT_KEYS as aok
from suwalski_assistant.tools import *
from suwalski_assistant.constants import AGENT_NAMES as an


class ImageTypeOutput(BaseModel):
    image_type: str = Field(description="'NOTES' if provided image contains handwritten note, 'OTHER' otherwise.")


def handle_handwritten_notes(callback_context: CallbackContext) -> Optional[types.Content]:
    state = ImageTypeOutput(**callback_context.state[aok.DETECTED_IMAGE_TYPE])
    image_type = state.image_type.strip().upper()

    if "NOTES" in image_type and "NOT NOTES" not in image_type:
        return content_from_text("Message has been handled, handwritten notes saved to Obsidian Vault.")
    return content_from_text("Image does not contain handwritten note. Call other agent to answer message.")


handwritten_notes_classifier_agent = LlmAgent(
    name=an.HANDWRITTEN_NOTES_CLASSIFIER_AGENT,
    model=ollama_model,
    instruction="Decide whether provided image contains handwritten notes.",
    output_schema=ImageTypeOutput,
    output_key=aok.DETECTED_IMAGE_TYPE,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
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

