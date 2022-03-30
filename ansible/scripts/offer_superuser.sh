#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../.."

source scripts/utils.sh

superuserexists_ret=0
docker-compose exec -T django poetry run ./manage.py superuserexists \
  || superuserexists_ret=$?
if (( superuserexists_ret == 1 )); then

  prompt "Would you like to create a superuser? [Y/n]" "Y"
  input_lower=${input,,}
  if [[ $input_lower == y ]]; then
    docker-compose exec django poetry run ./manage.py createsuperuser
  fi
fi
