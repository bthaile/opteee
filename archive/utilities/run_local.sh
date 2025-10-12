#!/bin/bash

# Stop and remove any existing container with the same name
docker stop opteee-options-search 2>/dev/null || true
docker rm opteee-options-search 2>/dev/null || true

# Build the image if it doesn't exist
docker build -t opteee-options-search .

# Run the container with environment variables from .env file
docker run -p 7860:7860 --env-file .env --name opteee-options-search opteee-options-search 