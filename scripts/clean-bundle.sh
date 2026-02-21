#!/bin/bash

# Navigate to the project root (one level up from the scripts directory)
cd "$(dirname "$0")/.." || exit 1

# Target directory
TARGET_DIR="./notes-assistant"

# Create target directory (re-create if exists)
echo "Preparing bundle in $TARGET_DIR..."
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"

# List of files to copy to root of bundle
FILES_TO_COPY=(
    "README.md"
    "pyproject.toml"
    ".env.example"
    ".env.llm-example"
    ".env.llm-local"
)

# Copy root files
for file in "${FILES_TO_COPY[@]}"; do
    if [ -f "$file" ]; then
        echo "Copying $file..."
        cp "$file" "$TARGET_DIR/"
    else
        echo "Warning: $file not found."
    fi
done

# Copy directories
if [ -d "src" ]; then
    echo "Copying src directory..."
    cp -r "src" "$TARGET_DIR/"
else
    echo "Warning: src directory not found."
fi

# Copy docs directory and its content
if [ -d "docs" ]; then
    echo "Copying docs content..."
    mkdir -p "$TARGET_DIR/docs"
    cp -r docs/* "$TARGET_DIR/docs/"
else
    echo "Warning: docs directory not found."
fi

# Copy deploy script
if [ -f "scripts/deploy/run.bat" ]; then
    echo "Copying run.bat to scripts/deploy/..."
    mkdir -p "$TARGET_DIR/scripts/deploy"
    cp "scripts/deploy/run.bat" "$TARGET_DIR/scripts/deploy/"
else
    echo "Warning: scripts/deploy/run.bat not found."
fi

echo "Renaming occurrences of 'suwalski' to 'notes' in $TARGET_DIR..."

# 1. Replace content in all files
# Use find with -type f to ensure we only process files
find "$TARGET_DIR" -type f -not -path '*/.*' -exec sed -i 's/Suwalski/Notes/g; s/suwalski/notes/g' {} +

# 2. Rename files and directories (bottom-up to avoid path invalidation)
# We handle both cases to ensure we catch everything
while IFS= read -r -d '' path; do
    new_path=$(echo "$path" | sed 's/Suwalski/Notes/g; s/suwalski/notes/g')
    if [ "$path" != "$new_path" ]; then
        echo "Renaming: $path -> $new_path"
        mv "$path" "$new_path"
    fi
done < <(find "$TARGET_DIR" -depth \( -name "*suwalski*" -o -name "*Suwalski*" \) -print0)

echo "Bundle created and sanitized successfully in $TARGET_DIR"
