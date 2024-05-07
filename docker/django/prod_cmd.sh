#!/bin/bash
set -e
source scripts/utils.sh

title_print "wait for database"
# https://docs.docker.com/compose/startup-order/
# Unfortunately this requires installing all Postgres client tools
# Alternatives:
#   - TCP port test
#   - Compile https://github.com/postgres/postgres/blob/master/src/bin/scripts/pg_isready.c
while ! pg_isready; do sleep 2; done

if [ "${DISABLE_BOOT_MIGRATE:-0}" -eq 0 ]; then
  title_print "migrate"
  dj migrate --no-input
fi

if [ "${DISABLE_BOOT_COLLECTSTATIC:-0}" -eq 0 ]; then
  title_print "collectstatic"
  dj collectstatic --noinput
fi

if [ "${DISABLE_BOOT_UPDATEGROUPS:-0}" -eq 0 ]; then
  title_print "updategroups"
  dj updategroups --sync
fi

title_print "gunicorn"
gunicorn project.wsgi:application --config docker/django/gunicorn_conf.py
