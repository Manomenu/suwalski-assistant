from typing import Optional, Literal
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from pydantic import BaseModel, Field
from suwalski_assistant.generic_agent import generic_agent
from suwalski_assistant.llm_models import ollama_model
from suwalski_assistant.constants import AGENTIC_OUTPUT_KEYS as aok
from suwalski_assistant.tools import *
from suwalski_assistant.constants import AGENT_NAMES as an
from suwalski_assistant.note_creator import save_note
import logging

class NoteMarkdownDataOutput(BaseModel):
    markdown_title: str
    markdown_content: str

class ImageTypeOutput(BaseModel):
    image_type: Literal["NOTES", "OTHER"] = Field(description="'NOTES' if provided image contains handwritten note, 'OTHER' otherwise.")


def detected_notes_condition(callback_context: CallbackContext) -> bool:
    state_data = callback_context.state[aok.DETECTED_IMAGE_TYPE]
    state = ImageTypeOutput(**state_data) if isinstance(state_data, dict) else state_data
    image_type = state.image_type.strip().upper()

    return image_type == "NOTES"

def try_get_markdown_note_data(callback_context: CallbackContext) -> Optional[NoteMarkdownDataOutput]:
    note_data = NoteMarkdownDataOutput(**callback_context.state.get(aok.NOTE_MARKDOWN_DATA))
            
    if note_data and note_data.markdown_title and note_data.markdown_content:
        return note_data
    return None


def try_default_user_response(callback_context: CallbackContext) -> Optional[types.Content]:
    if detected_notes_condition(callback_context):
       note_data = NoteMarkdownDataOutput(**callback_context.state.get(aok.NOTE_MARKDOWN_DATA))
       return content_from_text(f"Handwritten notes saved to Obsidian Vault as '{note_data.markdown_title}'")
    return None

def verify_handwritten_note_provided(callback_context: CallbackContext) -> Optional[types.Content]:
    state_data = callback_context.state[aok.DETECTED_IMAGE_TYPE]
    state = ImageTypeOutput(**state_data) if isinstance(state_data, dict) else state_data
    image_type = state.image_type.strip().upper()

    if image_type == "NOTES":
        return None
    return content_from_text("Image is not a note, so it cannot be turned into Obsidian note.")

def try_save_handwritten_note(callback_context: CallbackContext):
    logging.info(f"{an.HANDWIRTTEN_NOTES_CREATE_NOTE_AGENT}: trying to save handwritten note.")
    note_data = try_get_markdown_note_data(callback_context)
    if note_data:
        save_note(note_data.markdown_title, note_data.markdown_content)
    return None


handwritten_notes_classifier_agent = LlmAgent(
    name=an.HANDWRITTEN_NOTES_CLASSIFIER_AGENT,
    model=ollama_model,
    instruction="Decide whether provided image contains handwritten notes. NOTES - image contains handwritten notes, OTHER - image does not contains handwritten notes.",
    output_schema=ImageTypeOutput,
    output_key=aok.DETECTED_IMAGE_TYPE,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

response_for_user = LlmAgent(
    name=an.HANDWRITTEN_NOTES_RESPONSE_AGENT,
    model=ollama_model,
    instruction=f"You have to point out what does the provided image contains. Briefly, just one sentence.",
    before_agent_callback=try_default_user_response
)

create_markdown_note_agent = LlmAgent(
    name=an.HANDWIRTTEN_NOTES_CREATE_NOTE_AGENT,
    model=ollama_model,
    instruction="Transform image provided by user into markdown file. Returns markdown title to 'markdown_title' and markdown content to 'markdown_content'. Title shall be without / and \\ to avoid path issues.",
    output_key=aok.NOTE_MARKDOWN_DATA,
    output_schema=NoteMarkdownDataOutput,
    before_agent_callback=verify_handwritten_note_provided,
    after_agent_callback=try_save_handwritten_note
)

root_agent = SequentialAgent(
    name=an.HANDWRITTEN_NOTES_AGENT,
    description="""
        Checks whether provided image contains handwritten notes. If yes, then it parses it into markdown file and saves to Obsidian Vault.
    """,
    sub_agents=[handwritten_notes_classifier_agent, create_markdown_note_agent, response_for_user],
)

