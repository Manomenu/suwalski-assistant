#!/bin/bash

# Check if argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <environment_name>"
  echo "Example: $0 local (will use .env.local)"
  exit 1
fi

ENV_SUFFIX=$1
OVERRIDE_FILE=".env.${ENV_SUFFIX}"
DOTENV_FILE=".env"

# Check if override file exists
if [ ! -f "$OVERRIDE_FILE" ]; then
  echo "Error: Override file '$OVERRIDE_FILE' not found."
  exit 1
fi

# Check if .env exists
if [ ! -f "$DOTENV_FILE" ]; then
  echo "Warning: .env file not found. Creating a new one."
  touch "$DOTENV_FILE"
fi

echo "Configuring environment using $OVERRIDE_FILE..."

# Create a temporary file for the updated .env
NEW_DOTENV=$(mktemp)
cp "$DOTENV_FILE" "$NEW_DOTENV"

# Read the override file line by line
while IFS= read -r line || [ -n "$line" ]; do
  # Skip comments and empty lines
  [[ "$line" =~ ^#.* ]] && continue
  [[ -z "$line" ]] && continue

  # Extract key and value
  # This handles KEY=VALUE and KEY="VALUE"
  if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
    key="${BASH_REMATCH[1]}"
    value="${BASH_REMATCH[2]}"
    
    # Trim potential whitespace from key
    key=$(echo "$key" | xargs)

    # Check if the key exists in the current .env
    if grep -q "^${key}=" "$NEW_DOTENV"; then
      # Key exists, use sed to replace it. 
      # Using | as delimiter to handle potential / in values.
      # Note: This version of sed -i is compatible with most environments including Git Bash.
      sed -i "s|^${key}=.*|${key}=${value}|" "$NEW_DOTENV"
    else
      # Key doesn't exist, append it.
      # Ensure there's a newline before appending if the file isn't empty and doesn't end with one.
      [ -s "$NEW_DOTENV" ] && [ "$(tail -c 1 "$NEW_DOTENV" | wc -l)" -eq 0 ] && echo "" >> "$NEW_DOTENV"
      echo "${key}=${value}" >> "$NEW_DOTENV"
    fi
  fi
done < "$OVERRIDE_FILE"

# Move the updated file to .env
mv "$NEW_DOTENV" "$DOTENV_FILE"

echo "Successfully updated $DOTENV_FILE with values from $OVERRIDE_FILE."
