# Gemini Instructions & Project Context

This file provides context and technical guidelines for AI agents working on the Suwalski Assistant project.

## Technical Stack

- **Language:** Python 3.12+
- **Package Manager:** `uv` (Fast Python package installer and resolver)
- **Configuration:** `pyproject.toml` (PEP 517/518 compliant)
- **Frameworks:**
  - **Google Agent Development Kit (ADK):** Used for building and orchestrating intelligent agents.
  - **FastMCP:** Utilized for rapid development of MCP tools and servers.

## 🏗 Development Standards

- **Agentic-Oriented Programming:** All core agentic logic MUST leverage the **Google Agent Development Kit (ADK)**. Ensure all new features or scripts are AI-friendly and can be programmatically controlled.
- **Testing:** Comprehensive testing is required. See [tests/GEMINI.md](tests/GEMINI.md) for detailed guidelines and requirements.
- **Deployment:** The project must include scripts for preparing and validating a deployable bundle (e.g., `uv run build:bundle`).
- **Debugging:** A `.vscode/launch.json` must be maintained to allow for easy debugging of the assistant and its various components.
- **Modern Python:** Utilize type hints, `asyncio` where appropriate, and follow SOTA (State of the Art) design patterns for LLM-integrated applications.
- **Dependency Management:** Always use `uv` for adding or updating dependencies:
  ```bash
  uv add <package>
  uv run <command>
  ```

## 🤖 Agentic-Oriented Design

This project follows an **Agentic-Oriented Programming** paradigm. All aspects of configuration, management, and execution are designed to be easily discoverable and callable by AI programming agents.

- **AI-Callable Scripts:** Operations like swapping environment variables, restarting services, or clearing caches are encapsulated in semantic scripts (e.g., `uv run config:swap-env`).
- **Self-Documentation:** Codebase structure and tool definitions are optimized for machine readability to facilitate autonomous maintenance and evolution.
- **API-First Operations:** Management tasks expose interfaces that can be programmatically invoked by the assistant itself or external maintenance agents.

## 🏗 Architecture

The project is designed to run as a persistent service on a local network.

- **Host:** Private Server
- **Network:** Local Subnetwork
- **Integration Points:** Discord API, MCP Servers, Local System APIs

## 🤖 AI Guidelines

- **Tooling:** When creating new tools for the assistant, leverage the `fastmcp` decorator pattern for seamless integration.
- **Workflows:** Favor modular multi-agent architectures over single, massive prompt chains.
- **Environment:** Be mindful that the system runs on a private local server; prefer local integrations when possible.
