#!/bin/bash

# Stop and remove any existing container
docker stop wa-voice 2>/dev/null || true
docker rm wa-voice 2>/dev/null || true

# Build the image
docker build -t wa-voice:latest .

# Run the container
docker run -d -p 8085:8085 --name wa-voice wa-voice:latest

# Display running containers
docker ps
