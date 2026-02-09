# Suwalski Assistant

Suwalski Assistant is the core hub of a AI-powered system designed for seamless interaction, tool orchestration, and multi-agent workflows. It serves as the central intelligence hosted on a private local server.

## 🚀 Core Objectives

- **Unified Communication:** Facilitates interaction through multiple channels, starting with Discord, to provide a natural interface for system management and assistance.
- **Extensible Toolset:** A centralized place to define and manage custom tools that the AI agent can leverage to perform complex tasks.
- **Multi-Agent Orchestration:** Enables the definition and execution of complex workflows involving multiple specialized AI agents working in tandem.
- **MCP Integration:** Native support for the Model Context Protocol (MCP), allowing the assistant to integrate with a wide range of external data sources and tools.
- **Private & Secure:** Optimized for deployment on a private server within a local subnetwork, ensuring data privacy and low-latency performance.

## 🛠 Features

### Communication Gateways
- **Discord Integration:** (Planned/Active) Connect with the assistant via dedicated Discord channels.
- *Support for additional protocols can be defined here.*

### Agent Capabilities
- **Custom Tool Definitions:** Define specific functions and APIs the agent can call.
- **Workflow Management:** Orchestrate task handoffs and collaboration between different agent personas.
- **Handwritten Note Processing:** Automatically detects handwritten notes in images and saves them to the Obsidian Vault.

### Connectivity
- **MCP Tool Integration:** Seamlessly connect to MCP servers to extend the agent's knowledge and action space.

## 🚦 Getting Started

For detailed technical instructions, setup guides, and architectural context, please refer to [GEMINI.md](./GEMINI.md).

### Prerequisites
- Access to a private server environment
- Discord Bot Token (for Discord integration)

### Installation
```bash
# Example installation steps
git clone https://github.com/your-repo/suwalski-assistant.git
cd suwalski-assistant
# Follow instructions in GEMINI.md for setup
```

## 📜 License

[Specify License, e.g., MIT or Private]

## TODO
- Handle multiple images, so they get combined into one big note
- Obsidian manager - enhance note, fix note, add relevant links, Graph-RAG search app (integrated into discord chat) -> (MAYBE: create fully integrated NAS-native note AI-first app that integrates natively with discord)
- Add some assure message, that bot is working on processing image. (Inform about process if it takes longer)
- If Assistant isn't good to trust, then create explicit channel just for processing notes (you can add there text for some note formatting guidances - for example ask to aggregate shattered data, prettify it, etc., connect to other note?)
- For Note input create blocking behaviour, do not start processing next note, until previous one is processed. - it will save models from throttling. 
