import os
import logging
from suwalski_assistant.settings import settings

def save_note(title: str, content: str) -> str:
    """
    Saves a markdown note to the Obsidian vault path.
    Returns the path to the saved file.
    """
    vault_path = settings.obsidian_vault_path
    if not vault_path:
        logging.error("Obsidian vault path is not configured.")
        return "Error: Obsidian vault path is not configured."

    if not os.path.exists(vault_path):
        try:
            os.makedirs(vault_path, exist_ok=True)
        except Exception as e:
            logging.error(f"Failed to create vault directory: {e}")
            return f"Error: Failed to create vault directory: {e}"

    # Ensure title has .md extension
    if not title.endswith(".md"):
        filename = f"{title}.md"
    else:
        filename = title

    file_path = os.path.join(vault_path, f'DRAFT_{filename}')
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Note saved to {file_path}")
        return f"Note successfully saved to {file_path}"
    except Exception as e:
        logging.error(f"Failed to save note: {e}")
        return f"Error: Failed to save note: {e}"
