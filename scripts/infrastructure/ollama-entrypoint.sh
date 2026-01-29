#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
pid=$!

echo "Waiting for Ollama service to start..."
while ! ollama list > /dev/null 2>&1; do
    sleep 1
done

echo "Ollama service started."

# Pull the model if specified
if [ ! -z "$OLLAMA_MODEL" ]; then
    # Remove 'ollama/' prefix if present (e.g., 'ollama/qwen2:0.5b' -> 'qwen2:0.5b')
    MODEL_NAME=${OLLAMA_MODEL#ollama/}
    echo "Pulling model: $MODEL_NAME"
    ollama pull $MODEL_NAME
    echo "Model $MODEL_NAME pulled successfully."
fi

# Wait for Ollama process to finish.
wait $pid
