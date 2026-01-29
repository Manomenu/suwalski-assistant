#!/bin/bash

INPUT=${1}

# Check if input is a valid path
if [ -e "$INPUT" ]; then
  TARGET="$INPUT"
else
  # Try converting module to path assuming src/ root
  # Replace . with /
  PATH_FROM_MODULE="src/${INPUT//.//}.py"
  if [ -e "$PATH_FROM_MODULE" ]; then
    TARGET="$PATH_FROM_MODULE"
  else
    echo "Error: Could not find agent at '$INPUT' or '$PATH_FROM_MODULE'"
    exit 1
  fi
fi

echo "Running agent: $TARGET"
uv run adk run "$TARGET"