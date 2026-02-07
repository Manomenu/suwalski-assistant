from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from suwalski_assistant.llm_models import ollama_model

IMAGE_TYPE = "IMAGE_TYPE"

def handwritten_notes_after_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> LlmResponse | None:
    text_content = ""
    if llm_response.content and llm_response.content.parts:
        for part in llm_response.content.parts:
            if part.text:
                text_content += part.text

    if "NOTES" in text_content.strip().upper() and "NOT NOTES" not in text_content.upper():
        return LlmResponse(content=types.Content(parts=[types.Part(text="Notes saved to Obsidian Vault")]))
    return LlmResponse(content=types.Content(parts=[types.Part(text="Image does not contain handwritten note.")]))

root_agent = LlmAgent(
    name="handwritten_notes_agent",
    description="Identifies whether provided image is an handwritten note and saves it as markdown in Obsidian",
    model=ollama_model,
    instruction=f"""
        Decide whether given image contains handwritten notes. 
        Output *only* {IMAGE_TYPE}, it should be *only one word* 'NOTES' or 'OTHER'.
        Set {IMAGE_TYPE} to 'NOTES' if image contains handwritten notes, otherwise set type to 'OTHER'. 
    """,
    output_key=IMAGE_TYPE,
    after_model_callback=[handwritten_notes_after_callback]
)