from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from suwalski_assistant.llm_models import ollama_model
from suwalski_assistant.handwritten_notes_agent import handwritten_notes_agent

POSSIBLE_NOTE = "POSSIBLE_NOTE"

def validate_possible_note(callback_context: CallbackContext, llm_request: LlmRequest) -> None:
    has_image = "FALSE"

    for part in callback_context.user_content.parts:
        if part.text:
            return None
        if part.inline_data and part.inline_data and part.inline_data.mime_type.startswith('image/'):
            has_image = "TRUE"

    callback_context.state[POSSIBLE_NOTE] = has_image

root_agent = LlmAgent(
    name="entry_assistant",
    model=ollama_model,
    instruction="""
        You are a personal assistant. 
        You answer and do helpful actions. 
        You delegate tasks to subagents.

        If POSSIBLE_NOTE is TRUE: delegate job to *handwritten_notes_agent*.
    """,
    description="An assistant that delegates tasks to specialized subagents.",
    before_model_callback=[validate_possible_note],
    sub_agents=[handwritten_notes_agent]
)
