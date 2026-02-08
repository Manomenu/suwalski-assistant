from enum import StrEnum


class AGENTIC_STATES(StrEnum):
    POSSIBLE_NOTE = "POSSIBLE_NOTE"

class AGENTIC_OUTPUT_KEYS(StrEnum):
    DETECTED_IMAGE_TYPE = "DETECTED_IMAGE_TYPE"
    NOTE_MARKDOWN_DATA = "NOTE_MARKDOWN_DATA"

class AGENT_NAMES(StrEnum):
    HANDWRITTEN_NOTES_AGENT = "handwritten_notes_agent"
    HANDWRITTEN_NOTES_CLASSIFIER_AGENT = "handwritten_notes_classifier_agent"
    HANDWRITTEN_NOTES_RESPONSE_AGENT = "hn_image_describer_agent"
    HANDWIRTTEN_NOTES_CREATE_NOTE_AGENT = "create_markdown_note_agent"
    ENTRY_AGENT = "entry_assistant"
    GENERIC_AGENT = "generic_agent"