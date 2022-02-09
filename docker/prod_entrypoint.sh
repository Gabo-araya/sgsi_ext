#!/bin/bash
set -e
source scripts/utils.sh

title_print "Migrating..."
poetry run ./manage.py migrate

title_print "Running gunicorn..."
poetry run gunicorn project.wsgi:application --config docker/gunicorn_conf.py
