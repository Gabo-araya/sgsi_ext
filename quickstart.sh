#!/bin/bash
set -e
source scripts/utils.sh

# Create a local .env file if it does not exist
./scripts/env-init.sh

# Install docker and docker-compose
./scripts/docker-install.sh

# Build and start the containers
title_print 'Building containers...'
echo "docker-compose up --detach --build" | newgrp docker

# TODO: createsuperuser

# Done
color_print $green 'Completed! http://localhost:8000'
if [ -f quickstart-messages.log ]; then
  color_print $yellow "$(cat quickstart-messages.log)"
  rm quickstart-messages.log
fi
