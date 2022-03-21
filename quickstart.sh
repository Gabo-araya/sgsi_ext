#!/bin/bash
set -e
source scripts/utils.sh

# Create a local .env file if it does not exist
./scripts/env-init-dev.sh

# Install docker and docker-compose
./scripts/docker-install.sh

# Build and start the containers
title_print 'Building containers...'

if [[ ! -e docker-compose.override.yml ]]; then
  color_print "$cyan" "Linking compose override to dev version..."
  ln -s docker/docker-compose.dev.yml docker-compose.override.yml
fi

mkdir -p ~/.local/share/magnet-django-devcontainer/zshcustom

echo "docker-compose up --detach --build" | newgrp docker

# Set vscode to use python in poetry env
mkdir -p .vscode
if [[ ! -f .vscode/settings.json ]]; then
  poetryenv_path=$(echo \
    "docker-compose exec -T django poetry env info --path" |
    newgrp docker)

  echo \
'{
  "python.defaultInterpreterPath": "'"$poetryenv_path"'/bin/python",
}' > .vscode/settings.json

fi

# TODO: createsuperuser

# Done
color_print $green 'Completed! http://localhost:8000'
if [ -f quickstart-messages.log ]; then
  color_print $yellow "$(cat quickstart-messages.log)"
  rm quickstart-messages.log
fi
