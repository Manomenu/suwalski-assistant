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


handwritten_notes_classifier_agent = LlmAgent(
    name=an.HANDWRITTEN_NOTES_CLASSIFIER_AGENT,
    model=ollama_model,
    instruction="Decide whether provided image contains handwritten notes. NOTES - image contains handwritten notes, OTHER - image does not contains handwritten notes.",
    output_schema=ImageTypeOutput,
    output_key=aok.DETECTED_IMAGE_TYPE,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

formatter = LlmAgent(
    name="formatter",
    model=ollama_model,
    instruction="Writes down markdown file name and below writes markdown content. Take data from {note_markdown_data} if detected_image_type is NOTES. Otherwise inform that image is not a handwritten note."
)

class NoteMarkdownDataOutput(BaseModel):
    markdown_title: str
    markdown_content: str

def verify_if_can_create_note(callback_context: CallbackContext) -> Optional[types.Content]:
    state_data = callback_context.state[aok.DETECTED_IMAGE_TYPE]
    state = ImageTypeOutput(**state_data) if isinstance(state_data, dict) else state_data
    image_type = state.image_type.strip().upper()

    if image_type == "NOTES":
        return None
    return content_from_text("Image is not a note, so it cannot be turned into Obsidian note.")

create_markdown_note_agent = LlmAgent(
    name="create_markdown_note_agent",
    model=ollama_model,
    instruction="Transform image provided by user into markdown file. Returns markdown title to 'markdown_title' and markdown content to 'markdown_contnet'",
    output_key="note_markdown_data",
    output_schema=NoteMarkdownDataOutput,
    before_agent_callback=verify_if_can_create_note
)

root_agent = SequentialAgent(
    name=an.HANDWRITTEN_NOTES_AGENT,
    description="""
        Checks whether provided image contains handwritten notes. If yes, then it parses it into markdown file and saves to Obsidian Vault.
    """,
    sub_agents=[handwritten_notes_classifier_agent, create_markdown_note_agent, formatter],
)

