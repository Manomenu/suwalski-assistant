import logging
from pathlib import Path
from suwalski_assistant.settings import settings

def save_note(title: str, content: str) -> str:
    """
    Saves a markdown note to the Obsidian vault path.
    Returns the path to the saved file.
    """
    vault_path_str = settings.obsidian_vault_path
    if not vault_path_str:
        logging.error("Obsidian vault path is not configured.")
        return "Error: Obsidian vault path is not configured."

    # Use pathlib for more robust Windows/UNC path handling
    vault_path = Path(vault_path_str)

    if not vault_path.exists():
        try:
            vault_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.warning(f"Failed to create vault directory: {e}")

    # Ensure title has .md extension
    if not title.endswith(".md"):
        filename = f"{title}.md"
    else:
        filename = title

    file_path = vault_path / f'DRAFT_{filename}'
    
    try:
        with file_path.open("w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Note saved to {file_path}")
        return f"Note successfully saved to {file_path}"
    except Exception as e:
        logging.error(f"Failed to save note: {e}")
        return f"Error: Failed to save note: {e}"
