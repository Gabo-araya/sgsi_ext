#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
source scripts/utils.sh
should_be_inside_container

if [[ $DEBUG != "True" ]]; then
  color_print "$red" "DEBUG is not True."
  exit 1
fi

psql \
  -c 'drop database if exists "'"$PGDATABASE"'";' \
  -c 'drop database if exists "'"$PGDATABASE"'-logs";' \
  -c 'create database "'"$PGDATABASE"'";' \
  -c 'create database "'"$PGDATABASE"'-logs";' \
  postgres

./manage.py migrate # --yes-input
./manage.py migrate --database logs
