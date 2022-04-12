#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
source scripts/utils.sh
assert_outside_container

# Stop this project's postgres so port is free:
command -v docker-compose >/dev/null && [ -f .env ] && \
  echo "docker-compose stop postgres" | newgrp docker
scripts/assert-15432-free.sh

# Create a local .env file if it does not exist
scripts/env-init-dev.sh

# Install docker and docker-compose
scripts/docker-install.sh

# Determine usernames, UIDs and GIDs of current user
export WHO=$(whoami)
export HOST_UID=$(id -u)
export HOST_GID=$(id -g)

# Build and start the containers
title_print 'Building containers...'

if [[ ! -e docker-compose.override.yml ]]; then
  color_print "$cyan" "Linking compose override to dev version..."
  ln -s docker/docker-compose.dev.yml docker-compose.override.yml
fi

scripts/add-aliases.sh

newgrp docker <<EOF
docker-compose build && \
docker-compose down && \
docker-compose run django docker/django/venv_to_dotenv.sh .env && \
docker-compose up --detach
EOF
# "down" because https://github.com/docker/compose/issues/4548

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
  echo "docker-compose exec -T django dj migrate" | newgrp docker

  superuserexists_ret=0
  echo "docker-compose exec -T django dj superuserexists" | newgrp docker \
    || superuserexists_ret=$?
  if (( superuserexists_ret == 1 )); then

    prompt "\n\nWould you like to create a superuser? [Y/n]" "Y"
    input_lower=${input,,}
    if [[ $input_lower == y ]]; then
      # Black magic: normally newgrp reads commands from pipe,
      # so can't get keyboard answers to createsuperuser.  https://www.scosales.com/ta/kb/104260.html
      exec 3<&0
      echo "exec \
        docker-compose exec django dj createsuperuser \
        0<&3 3<&-" | newgrp docker
      echo -e "\n"
    fi
  fi
fi

# Done
color_print $green 'Completed!'

if [ -f quickstart-messages.log ]; then
  color_print $yellow "$(cat quickstart-messages.log)"
  rm quickstart-messages.log
fi

color_print $green "After rebooting if required,
open this folder in VSCode,
install the recommended 'Remote - Containers' extension if prompted,
and click 'Reopen in Container' when prompted. (Or press F1 and type 'Reopen in Container')

Then in a VSCode terminal (if a black-and-white one appears (bash), press ctrl-D and open a new one),
run 'dj runserver' and access the site at http://localhost:8000"
