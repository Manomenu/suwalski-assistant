from typing import Optional
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from suwalski_assistant.llm_models import base_model
from suwalski_assistant.handwritten_notes_agent import handwritten_notes_agent
from suwalski_assistant.generic_agent import generic_agent
from suwalski_assistant.constants import *
from suwalski_assistant.helpers import *

def rule_wrapper(text: str) -> str:
    return f'<RULE>{text}</RULE>'

def consider_possible_note(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    has_image = False
    forbid_rule = rule_wrapper(f"You are not allowed to call *{AGENT_NAMES.HANDWRITTEN_NOTES_AGENT}*.")
    do_rule = rule_wrapper(f"Your should in the first place call *{AGENT_NAMES.HANDWRITTEN_NOTES_AGENT}*.")

    for part in callback_context.user_content.parts:
        if part.text:
            append_part_to_request(llm_request, forbid_rule)
            return None

        if part.inline_data and part.inline_data and part.inline_data.mime_type.startswith('image/'):
            has_image = True

    if not has_image:
        append_part_to_request(llm_request, forbid_rule)
    else:
        append_part_to_request(llm_request, do_rule)
    return None

generic_rule = rule_wrapper(f"If there is no other suggestion delegate a job to *{AGENT_NAMES.GENERIC_AGENT}*")

root_agent = LlmAgent(
    name=AGENT_NAMES.ENTRY_AGENT,
    model=base_model,
    instruction=f"""
        You are a personal assistant. 
        You answer and do helpful actions. 
        You delegate tasks to subagents.

        
        Obey all Rules in format {rule_wrapper('rule_contnet')} regarding sub_agent calling.
        
        {generic_rule}
    """,
    description="An assistant that delegates tasks to specialized subagents.",
    before_model_callback=[consider_possible_note],
    sub_agents=[handwritten_notes_agent, generic_agent]
)


