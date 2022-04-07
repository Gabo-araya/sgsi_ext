#!/bin/bash

# This is a shortcut to run django commands in a server.
# For example, you can get to a django shell with:
#   ./dj.sh shell

set -euo pipefail
cd "$(dirname "$0")"
source scripts/utils.sh

if ! grep -q docker /proc/1/cgroup; then
  # Outside container
  docker-compose exec django dj "$@"
else
  color_print "$cyan" 'Note: this script is useful outside the container. Inside, you can use "dj"'
  exec dj "$@"
fi


# TODO: delete this script. Replace it by making deploy.yml set this:
#   alias dj="dce django dj"

# This made sense when its content would be:
#   docker-compose -f docker-compose.yml -f docker/docker-compose.prod.yml exec django poetry run ./manage.py "$@"
# but not anymore.
