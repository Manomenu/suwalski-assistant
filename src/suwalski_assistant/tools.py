from google.genai import types
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

def content_from_text(text: str) -> types.Content:
    return types.Content(role='model', parts=[types.Part(text=text)])

def modify_response_last_content(response: LlmResponse, text: str) -> LlmResponse:
    response.content[-1] = content_from_text(content_from_text(text))
    return response

def append_part_to_request(llm_request: LlmRequest, part_text: str) -> LlmRequest:
    if not len(llm_request.contents):
        llm_request.contents.append(types.Content(parts=[]))
    llm_request.contents[-1].parts.append(types.Part(text=part_text))
    return llm_request

