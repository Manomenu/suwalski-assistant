from asyncio import Lock
from queue import Queue
from typing import Any, Awaitable, Callable
from google.genai import types
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

def content_from_text(text: str) -> types.Content:
    return types.Content(role='model', parts=[types.Part(text=text)])

def modify_response_last_content(response: LlmResponse, text: str) -> LlmResponse:
    response.content[-1] = content_from_text(text)
    return response

def append_part_to_request(llm_request: LlmRequest, part_text: str) -> LlmRequest:
    if not len(llm_request.contents):
        llm_request.contents.append(types.Content(parts=[]))
    llm_request.contents[-1].parts.append(types.Part(text=part_text))
    return llm_request


class MessageQueue:
    def __init__(self):
        self._queue = Queue()
        self._lock = Lock()
        self._is_consuming = False

    async def add(self, message):
        async with self._lock:
            self._queue.put(message)

    async def try_consume(self, consume_process: Callable[[Any], Awaitable]) -> bool:
        async with self._lock:
            if self._is_consuming:
                return False
            self._is_consuming = True

            if self._queue.empty():
                self._is_consuming = False
                return False

            message = self._queue.get()

        await consume_process(message)

        async with self._lock:
            self._is_consuming = False
        
        return True
