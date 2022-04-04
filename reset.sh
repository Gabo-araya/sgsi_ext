#!/bin/bash
set -euo pipefail
source scripts/utils.sh

if [[ $DEBUG != "True" ]]; then
  color_print "$red" "DEBUG is not True."
  exit 1
fi

psql \
  -c "drop database if exists \"$PGDATABASE\";" \
  -c "create database \"$PGDATABASE\";" \
  postgres

dj migrate
