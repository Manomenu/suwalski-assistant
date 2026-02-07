from enum import StrEnum


class AGENTIC_STATES(StrEnum):
    POSSIBLE_NOTE = "POSSIBLE_NOTE"

class AGENTIC_OUTPUT_KEYS(StrEnum):
    DETECTED_IMAGE_TYPE = "DETECTED_IMAGE_TYPE"

class AGENT_NAMES(StrEnum):
    HANDWRITTEN_NOTES_AGENT = "handwritten_notes_agent"
    HANDWRITTEN_NOTES_CLASSIFIER_AGENT = "handwritten_notes_agent_classifier"
    ENTRY_AGENT = "entry_assistant"
    GENERIC_AGENT = "generic_agent"