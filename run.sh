#!/bin/bash

# Check dependencies
if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
    echo "Error: Docker and Docker Compose are required."
    exit 1
fi

# Build images
echo "\nBuilding Docker images..."
docker compose build || { echo "Build failed"; exit 1; }

# Start services (except agent if it is only for tests)
echo "\nStarting target service..."
docker compose up -d target || { echo "Startup failed"; exit 1; }

# Wait for services to be ready
echo "\nWaiting for services to be ready..."
sleep 5

# Run tests in the agent container (once)
echo -e "\n=== Test Report ==="
docker compose run --rm agent pytest -v --maxfail=1 -W always || { echo "\nTests failed"; exit 1; }

# Stop containers
echo -e "\n=== Stopping Containers ==="
docker compose down