#!/bin/bash
set -e
source scripts/utils.sh

env_file='docker/development.env'

# Create a new env file if it does not exist
if [ -f "$env_file" ]; then
  echo "Using existing development.env"
else
  color_print $cyan 'Creating development.env file...'
  cp "$env_file.example" "$env_file"
  color_print $green 'Done'
fi

# Build and start the containers
color_print $cyan 'Building containers...'
docker-compose up --detach --build

# Done
color_print $green 'Completed! http://localhost:8000'
