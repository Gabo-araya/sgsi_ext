#!/bin/bash
set -e
source scripts/utils.sh

# Create a local .env file if it does not exist
./scripts/env-init-dev.sh

# Install docker and docker-compose
./scripts/docker-install.sh

# Build and start the containers
title_print 'Building containers...'
echo "docker-compose up --detach --build" | newgrp docker

# TODO: createsuperuser

# Ensure ownership of db_dumps/
[ -O db_dumps/ ] || sudo chown "$UID:$(id -g)" db_dumps/

# Done
color_print $green 'Completed! http://localhost:8000'
if [ -f quickstart-messages.log ]; then
  color_print $yellow "$(cat quickstart-messages.log)"
  rm quickstart-messages.log
fi
