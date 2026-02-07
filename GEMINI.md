# Gemini Instructions & Project Context

This file provides context and technical guidelines for AI agents working on the Suwalski Assistant project.

## 🛠 Technical Stack

- **Language:** Python 3.12+
- **Package Manager:** `uv` (Fast Python package installer and resolver) (pyproject.toml used)
- **Containerization:** Docker & Docker Compose
- **Frameworks:**
  - **Google Agent Development Kit (ADK):** Used for building and orchestrating intelligent agents.
  - **FastMCP:** Utilized for rapid development of MCP tools and servers.
  - **Ollama:** Local LLM inference (Default: `qwen2:0.5b`).

## 🏗 Development Standards

- **Agentic-Oriented Programming:** All core agentic logic MUST leverage the **Google Agent Development Kit (ADK)** using `InMemoryRunner`.
- **Testing:** Comprehensive testing is required. See [tests/GEMINI.md](tests/GEMINI.md).
- **Package Initialization (`__init__.py`):** Leverage `__init__.py` files to alias generic/framework-required names to semantic ones within the project scope. For example, always expose the required `root_agent` as a more meaningful name (e.g., `ollama_agent = root_agent`) to improve code discoverability and readability.
- **Debugging:** A `.vscode/launch.json` is maintained for VS Code debugging, utilizing tasks to auto-start infrastructure.
- **Dependency Management:**
- **Comments in Code** Comments are minimalistic, they do not expain code that is self-explanatory. Comment added only if necessary. 
  ```bash
  uv add <package>
  uv run <command>
  ```

## 🚀 Development Workflow

### Infrastructure vs. Application Strategy
We strictly separate infrastructure from application logic during development to enable fast iteration and easy debugging.

1.  **Infrastructure:** Managed via `docker-compose.yml` (Ollama, Databases).
    - **Start:** `scripts/infrastructure/infra-up.sh` (or auto-started via VS Code).
    - **Note:** The `ollama` service includes an entrypoint that automatically pulls the required model (default: `qwen2:0.5b`).

2.  **Application:** Run locally via `uv` or VS Code.
    - **Start:** `scripts/start.sh` or VS Code "Debug: Main App".

### Docker Profiles
- **Default:** Runs infrastructure only.
- **Profile `fullstack`:** Runs Infrastructure + Containerized App (for integration testing/production).
  - **Start:** `scripts/fullstack-up.sh`
  - **Stop:** `scripts/fullstack-down.sh`

## 🤖 Agentic-Oriented Design

- **AI-Callable Scripts:** Operations are encapsulated in semantic scripts in `scripts/`.
- **Self-Documentation:** Codebase structure is optimized for AI understanding.
- **API-First Operations:** Management tasks are programmatic.

## 🏗 Architecture

- **Host:** Private Server (Local Subnetwork)
- **Runtime:** Python 3.12 (Local) / Docker (Prod)
- **Integration Points:** Discord API, MCP Servers, Local System APIs, Ollama (Local LLM)