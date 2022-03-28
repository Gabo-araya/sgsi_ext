#!/bin/bash

if grep -q "^VIRTUAL_ENV=" "$1"; then
  # Already present
  exit
fi

source "$(cd /usr/src/app && poetry env info --path)/bin/activate"

cat <<EOF >>"$1"

# Automatically enable virtualenv:
VIRTUAL_ENV=$VIRTUAL_ENV
PATH=$PATH
EOF
