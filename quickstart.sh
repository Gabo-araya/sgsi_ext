#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
source scripts/utils.sh

# Assert we're running on a recent bash
if [[ "$BASH_VERSINFO" -lt 4 ]]; then
  color_print $red "This script requires GNU bash version 4 or later.
Please upgrade your system utilities and try again."
  exit 1
fi

assert_outside_container

# Assert not root
if (( EUID == 0 )); then
  color_print $red "Please run this script without sudo."
  # Because sudo is used internally when required.
  # Otherwise regular files would be created with owner as root
  # and would require sudo later at various points.
  # Also HOST_UID/GID would be set to 0 (although this could be handled with SUDO_UID/GID).
  exit 1
fi

# Check if the host OS does support file execute permissions. If this is not
# the case, abort this script.
assert_fs_supports_exec_permission

if [[ "$OSTYPE" == darwin* ]]; then
    message="WARNING: Django 3 Project Template has not been thoroughly tested on
macOS systems. Expect things to break while running on this configuration.
You have been warned."
    color_print "$yellow" "$message"
fi

# Stop this project's postgres so port is free:
command -v docker-compose >/dev/null && [ -f .env ] && \
  echo "docker-compose stop postgres || true" | newgrp docker
scripts/assert-15432-free.sh

# Create a local .env file if it does not exist
scripts/env-init-dev.sh

# Install docker and docker-compose
scripts/docker-install.sh

# Build and start the containers
title_print 'Building containers...'

if [[ ! -e docker-compose.override.yml ]]; then
  color_print "$cyan" "Linking compose override to dev version..."
  ln -s docker/docker-compose.dev.yml docker-compose.override.yml
fi

scripts/add-aliases.sh

echo "docker-compose build && docker-compose down" | newgrp docker
# "down" because https://github.com/docker/compose/issues/4548

# Now that the image is built, set virtual_env in .env:
env_file='.env'
# VIRTUAL_ENV must be unset for poetry to generate the path itself
virtual_env=$(echo "docker-compose run --rm -T django env --unset=VIRTUAL_ENV poetry env info --path" | newgrp docker)
perl -pi -e "s|{{virtual_env}}|$virtual_env|g" $env_file

# Set vscode to use python in poetry env
mkdir -p .vscode
if [[ ! -f .vscode/settings.json ]]; then
  echo \
"{
  \"python.defaultInterpreterPath\": \"$virtual_env/bin/python\",
}" > .vscode/settings.json
fi

# Finally create and start the containers:
echo "docker-compose up --detach" | newgrp docker

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

color_print $green 'After rebooting if required,
- Open this folder in VSCode
- Click "Install" when prompted to install the recommended extensions for this repository
- Then click "Reopen in Container" when prompted (or press F1 and choose "Reopen in Container")

Then in a VSCode terminal run "npm start",
and in another terminal, run "djs" and access the site at http://localhost:8000'
