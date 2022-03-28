#!/bin/bash

source "$(cd /usr/src/app && poetry env info --path)/bin/activate"

cat <<EOF >>"$1"

# Automatically enable virtualenv:
VIRTUAL_ENV=$VIRTUAL_ENV
PATH=$PATH
EOF
