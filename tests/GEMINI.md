# Testing Guidelines

This file provides context and technical guidelines for testing the Suwalski Assistant project.

## 🧪 Testing Requirements

- **Location:** All tests must reside in the `/tests` directory.
- **Mandatory Passing:** A successful test run is a strict requirement for any deployable bundle. No code should be merged or deployed if tests are failing.
- **Framework:** (Specify framework here, e.g., `pytest`).
- **Coverage:** Aim for high test coverage, especially for critical agentic workflows and tool integrations.

## 🤖 AI Testing Standards
- **Mocking:** Extensively mock external APIs (Discord, MCP servers) to ensure tests are fast and deterministic.
- **Integration Tests:** Include integration tests that verify the interaction between the agent, the ADK, and local tools.
