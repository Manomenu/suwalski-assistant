from typing import Optional, Literal
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from pydantic import BaseModel, Field
from suwalski_assistant.llm_models import vision_model, base_model
from suwalski_assistant.constants import AGENTIC_OUTPUT_KEYS as aok
from suwalski_assistant.helpers import *
from suwalski_assistant.constants import AGENT_NAMES as an
from suwalski_assistant.services.note_creator import save_note
from suwalski_assistant.settings import settings
import logging


def sanitize_title(title: str) -> str:
    return title.replace("/", "_").replace("\\", "_")


class NoteMarkdownDataOutput(BaseModel):
    markdown_title: str
    markdown_content: str

class ImageTypeOutput(BaseModel):
    image_type: Literal["NOTES", "OTHER"] = Field(description="'NOTES' if provided image contains handwritten note, 'OTHER' otherwise.")


def detected_notes_condition(callback_context: CallbackContext) -> bool:
    logging.debug(f"{an.HANDWRITTEN_NOTES_AGENT}: Checking if image contains notes.")
    state_data = callback_context.state[aok.DETECTED_IMAGE_TYPE]
    state = ImageTypeOutput(**state_data) if isinstance(state_data, dict) else state_data
    image_type = state.image_type.strip().upper()

    return image_type == "NOTES"

def try_get_markdown_note_data(callback_context: CallbackContext) -> Optional[NoteMarkdownDataOutput]:
    logging.debug(f"{an.HANDWRITTEN_NOTES_AGENT}: Attempting to retrieve markdown note data from state.")
    note_data_raw = callback_context.state.get(aok.NOTE_MARKDOWN_DATA)
    if not note_data_raw:
        return None
        
    note_data = NoteMarkdownDataOutput(**note_data_raw) if isinstance(note_data_raw, dict) else note_data_raw
            
    if note_data and note_data.markdown_title and note_data.markdown_content:
        return note_data
    return None


def try_default_user_response(callback_context: CallbackContext) -> Optional[types.Content]:
    logging.info(f"{an.HANDWRITTEN_NOTES_RESPONSE_AGENT}: Executing before_agent_callback to check for default response.")
    if detected_notes_condition(callback_context):
       note_data = try_get_markdown_note_data(callback_context)
       if note_data:
           return content_from_text(f"Handwritten notes saved to {settings.notes_location_name} as '{sanitize_title(note_data.markdown_title)}'")
    return None

def verify_handwritten_note_provided(callback_context: CallbackContext) -> Optional[types.Content]:
    logging.info(f"{an.HANDWIRTTEN_NOTES_CREATE_NOTE_AGENT}: Executing before_agent_callback to verify note presence.")
    state_data = callback_context.state[aok.DETECTED_IMAGE_TYPE]
    state = ImageTypeOutput(**state_data) if isinstance(state_data, dict) else state_data
    image_type = state.image_type.strip().upper()

    if image_type == "NOTES":
        return None
    return content_from_text(f"Image is not a note, so it cannot be turned into {settings.notes_location_name} note.")

def try_save_handwritten_note(callback_context: CallbackContext):
    logging.info(f"{an.HANDWIRTTEN_NOTES_CREATE_NOTE_AGENT}: Executing after_agent_callback to save handwritten note.")
    note_data = try_get_markdown_note_data(callback_context)
    if note_data:
        # Sanitize title to avoid path issues
        sanitized_title = sanitize_title(note_data.markdown_title)
        logging.info(f"{an.HANDWIRTTEN_NOTES_CREATE_NOTE_AGENT}: Saving note with title: {sanitized_title}")
        save_note(sanitized_title, note_data.markdown_content)
    return None


handwritten_notes_classifier_agent = LlmAgent(
    name=an.HANDWRITTEN_NOTES_CLASSIFIER_AGENT,
    model=vision_model,
    instruction="Decide whether last provided image contains handwritten note. NOTES - image contains handwritten notes, OTHER - image does not contains handwritten notes.",
    output_schema=ImageTypeOutput,
    output_key=aok.DETECTED_IMAGE_TYPE,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

def clean_up_session_data(callback_context: CallbackContext):
    for event in callback_context.session.events:
        event.content.parts = [part for part in event.content.parts if not part.inline_data or not isinstance(part.inline_data, types.Blob)]
    callback_context.session.events = [event for event in callback_context.session.events if len(event.content.parts) > 0]
    

response_for_user = LlmAgent(
    name=an.HANDWRITTEN_NOTES_RESPONSE_AGENT,
    model=base_model,
    instruction=f"Based on previous descriptions of image describe what did it contain. Briefly, just one sentence.",
    before_agent_callback=try_default_user_response
)

create_markdown_note_agent = LlmAgent(
    name=an.HANDWIRTTEN_NOTES_CREATE_NOTE_AGENT,
    model=vision_model,
    instruction="Transform image provided by user into markdown file. Returns markdown title to 'markdown_title' and markdown content to 'markdown_content'. Title shall be without / and \\ to avoid path issues. Write down every word included in a note so it is complete.",
    output_key=aok.NOTE_MARKDOWN_DATA,
    output_schema=NoteMarkdownDataOutput,
    before_agent_callback=verify_handwritten_note_provided,
    after_agent_callback=try_save_handwritten_note
)

root_agent = SequentialAgent(
    name=an.HANDWRITTEN_NOTES_AGENT,
    description=f"""
        Checks whether provided image contains handwritten notes. If yes, then it parses it into markdown file and saves to {settings.notes_location_name}.
    """,
    sub_agents=[handwritten_notes_classifier_agent, create_markdown_note_agent, response_for_user],
    after_agent_callback=clean_up_session_data
)

