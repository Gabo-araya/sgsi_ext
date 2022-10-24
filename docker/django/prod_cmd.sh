#!/bin/bash
set -e
source scripts/utils.sh

if ! [[ -d "$VIRTUAL_ENV" ]]; then
  color_print $red "Error: \$VIRTUAL_ENV is not a directory. Please fix env var and recreate container."
  exit 1
fi

title_print "wait for database"
# https://docs.docker.com/compose/startup-order/
# Unfortunately this requires installing all Postgres client tools
# Alternatives:
#   - TCP port test
#   - Compile https://github.com/postgres/postgres/blob/master/src/bin/scripts/pg_isready.c
while ! pg_isready; do sleep 2; done

title_print "migrate"
dj migrate --no-input
# TODO: add option to disable automatic migrations, and script to help in manual migrations

title_print "collectstatic"
dj collectstatic --noinput

title_print "gunicorn"
gunicorn project.wsgi:application --config docker/django/gunicorn_conf.py
