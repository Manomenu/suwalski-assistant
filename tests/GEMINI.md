# Testing Guidelines

This file provides context and technical guidelines for testing the Suwalski Assistant project.

## 🧪 Testing Requirements

- **Location:** All tests must reside in the `/tests` directory.
- **Mandatory Passing:** A successful test run is a strict requirement for any deployable bundle.
- **Framework:** `pytest` (Run via `scripts/test.sh` or `uv run pytest`).
- **Coverage:** Aim for high test coverage, especially for critical agentic workflows and tool integrations.

## 🤖 AI Testing Standards

- **Agentic Logic:** Tests for agents should mock external dependencies.
- **Mocking:**
  - **Ollama/LLMs:** Do not connect to real LLMs during unit tests. Mock `LiteLlm` or the `Runner` interactions.
  - **ADK Components:** Mock `InMemoryRunner` or `SessionService` where appropriate to isolate unit logic.
- **Integration Tests:**
  - Full integration tests requiring real infrastructure should be marked (e.g., `@pytest.mark.integration`) and may require `scripts/infrastructure/infra-up.sh` to be running.