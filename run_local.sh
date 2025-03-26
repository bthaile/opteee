#!/bin/bash

# Build the image if it doesn't exist
docker build -t opteee-options-search .

# Run the container with environment variables from .env file
docker run -p 7860:7860 --env-file .env opteee-options-search 