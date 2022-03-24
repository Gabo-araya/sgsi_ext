#!/bin/bash

# This is a shortcut to run django commands in a server.
# For example, you can get to a django shell with:
#   ./dj.sh shell

docker-compose exec django poetry run ./manage.py "$@"
