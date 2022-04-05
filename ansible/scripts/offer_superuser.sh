#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../.."
source scripts/utils.sh
assert_outside_container

superuserexists_ret=0
docker-compose exec -T django dj superuserexists \
  || superuserexists_ret=$?
if (( superuserexists_ret == 1 )); then

  prompt "Would you like to create a superuser? [Y/n]" "Y"
  input_lower=${input,,}
  if [[ $input_lower == y ]]; then
    docker-compose exec django dj createsuperuser
  fi
fi
