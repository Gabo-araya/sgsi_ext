#!/bin/bash
set -e
poetry run ./manage.py migrate
poetry run gunicorn project.wsgi:application --config docker/gunicorn_conf.py
