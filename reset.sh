#!/bin/bash
set -euo pipefail
source scripts/utils.sh

if [[ $DEBUG != "True" ]]; then
  color_print "$red" "DEBUG is not True."
  exit 1
fi

color_print "$cyan" "dropdb $PGDATABASE"
drop_status=0
drop_output=$(dropdb "$PGDATABASE") || drop_status=$?
# Fail if dropdb failed, except in case of "does not exist"
if [[ $drop_status != 0 && "$drop_output" != *" does not exist" ]]; then
  echo "$drop_output"
  exit $drop_status
fi

color_print "$cyan" "createdb $PGDATABASE"
createdb "$PGDATABASE"

color_print "$cyan" "./manage.py migrate"
./manage.py migrate
