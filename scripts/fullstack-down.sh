#!/bin/bash
echo "Shutting down full stack..."
docker-compose --profile fullstack down
echo "Full stack shut down successfully."
