#!/bin/bash

if grep -q "^VIRTUAL_ENV=" "$1"; then
  # Already present
  exit
fi

if [[ -z "$VIRTUAL_ENV" ]]; then
  source "$(cd /usr/src/app && poetry env info --path)/bin/activate"
  # Note: it only activates for the bash running this script.
  # Conditional activation to prevent duplicating venv path.
fi

cat <<EOF >>"$1"

# Automatically enable virtualenv:
VIRTUAL_ENV=$VIRTUAL_ENV
PATH=$PATH
EOF
