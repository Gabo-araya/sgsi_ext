#!/bin/bash
set -e
source scripts/utils.sh

env_file='docker/development.env'

# Create a new env file if it does not exist
title_print "Checking .env files..."
if [ -f "$env_file" ]; then
  echo "Using existing development.env"
else
  echo "Creating development.env file..."
  cp "$env_file.example" "$env_file"
fi
color_print $green 'Done'

# Install docker and docker-compose
./scripts/docker-install.sh

# Build and start the containers
title_print 'Building containers...'
docker-compose up --detach --build

# Done
color_print $green 'Completed! http://localhost:8000'
