#!/bin/bash
set -e
source scripts/utils.sh

title_print "migrate"
poetry run ./manage.py migrate

title_print "collectstatic"
poetry run ./manage.py collectstatic --noinput

title_print "gunicorn"
poetry run gunicorn project.wsgi:application --config docker/gunicorn_conf.py
