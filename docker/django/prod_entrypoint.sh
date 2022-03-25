#!/usr/bin/env bash

# Source poetry virtualenv so "poetry run" is not required.
source "venv_path_to_be_replaced_in_dockerfile/bin/activate"

exec "$@"
