#!/bin/bash
echo "Stopping infrastructure (Ollama)..."
docker-compose down ollama
echo "Infrastructure stopped."
