# Setup
0. Make sure you have `python` (>=3.12) installed. Then make sure you have `uv` installed as global package (run `pip install uv`).
1. Create discord bot with permissions to read/write on discord server and add it to target server. While creating that bot save token value to be later pasted into `DISCORD_TOKEN` variable.
2. Save channel id of the channel that you want the bot to interact with. Will be pasted into `DISCORD_CHANNEL_ID`.
3. Create `.env` file in notes_assistant directory.
4. Paste `.env.example` content into `.env` and fill data with proper values. Example:
```
DISCORD_TOKEN=described_above
DISCORD_CHANNEL_ID=described_above
NOTES_PATH=//XXX.XXX.X.XXX/nas-main-folder/obsidian-vault-folder # or any local filesystem folder location (path)
NOTES_LOCATION_NAME=Obsidian Vault
LLM_ENV=llm-local
INPUT_MODE=discord
```
5. Fill `.env.llm-local` with proper LLM (AI/Chatbot) credentials & link. I suggest asking how do get this data by asking Gemini/ChatGPT (mention your LLM provider, for example ollama cloud (they offer free models sometimes) and that those arguments shall fit `LiteLLM` class python schema `(model, api_key, api_base)` arguments). Example (you can check on the internet model alternatives, but this combination works good enough):
```
BASE_MODEL=openai/gpt-oss:20b
BASE_API_KEY=sk-...
BASE_API_BASE=https://my-webui-website.com/ollama/v1

VISION_MODEL=openai/qwen3-vl:32b
VISION_API_KEY=sk-...
VISION_API_BASE=https://my-webui-website.com/ollama/v1
LLM_ENV=llm-local
```
6. Open Task Scheduler, create new task, that is run on startup as SYSTEM (not current user), set triggered action to run script `scripts/deploy/run.bat`. You can then select that task and Run to start bot immediatelly (or restart a PC/server).  