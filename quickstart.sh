#!/bin/bash
set -euo pipefail
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

newgrp docker <<EOF
docker-compose build && \
docker-compose run django docker/django/venv_to_dotenv.sh .env && \
docker-compose up --detach --force-recreate
EOF

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

prompt "\n\nWould you like to run migrations? [Y/n]" "Y"
input_lower=${input,,}
if [[ $input_lower == y ]]; then
  echo "docker-compose exec -T django poetry run ./manage.py migrate" | newgrp docker

  superuserexists_ret=0
  echo "docker-compose exec -T django poetry run ./manage.py superuserexists" | newgrp docker \
    || superuserexists_ret=$?
  if (( superuserexists_ret == 1 )); then

    prompt "\n\nWould you like to create a superuser? [Y/n]" "Y"
    input_lower=${input,,}
    if [[ $input_lower == y ]]; then
      # Black magic: normally newgrp reads commands from pipe,
      # so can't get keyboard answers to createsuperuser.  https://www.scosales.com/ta/kb/104260.html
      exec 3<&0
      echo "exec \
        docker-compose exec django poetry run ./manage.py createsuperuser \
        0<&3 3<&-" | newgrp docker
      echo -e "\n"
    fi
  fi
fi

# Done
color_print $green 'Completed! http://localhost:8000'
if [ -f quickstart-messages.log ]; then
  color_print $yellow "$(cat quickstart-messages.log)"
  rm quickstart-messages.log
fi
