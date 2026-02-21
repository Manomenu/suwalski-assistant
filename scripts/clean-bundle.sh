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
        cp "$file" "$TARGET_DIR/"
    else
        echo "Warning: $file not found."
    fi
done

# Copy directories
if [ -d "src" ]; then
    cp -r src "$TARGET_DIR/"
fi

# Copy contents of docs
if [ -d "docs" ]; then
    mkdir -p "$TARGET_DIR/docs"
    cp -r docs/* "$TARGET_DIR/docs/"
fi

# Copy deploy script
if [ -f "scripts/deploy/run.bat" ]; then
    cp "scripts/deploy/run.bat" "$TARGET_DIR/"
else
    echo "Warning: scripts/deploy/run.bat not found."
fi

echo "Bundle created successfully in $TARGET_DIR"
