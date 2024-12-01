#!/bin/sh

# Stop and remove containers, networks, and volumes defined in the docker-compose.yml
docker-compose down -v

# Get the image ID for the web service
IMAGE_ID=$(docker images -q "refferalsystemdjango-web")

# Check if the image ID is not empty and remove the image
if [ -n "$IMAGE_ID" ]; then
  docker rmi "$IMAGE_ID"
else
  echo "No images to remove."
fi