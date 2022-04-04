#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
source ../scripts/utils.sh
should_be_inside_container

if (( $# == 0 )); then
  echo "Please specify target server"
  exit 1
fi
target=$1

readonly LOCAL_DUMPS_PATH=../db_dumps

if (( $# == 1 )); then
  create_dump_limit=$target
  source scripts/create_dump.sh
else
  dump_name=$2
fi

local_dump_path="$LOCAL_DUMPS_PATH/$dump_name"

if [ ! -f "$local_dump_path" ]; then
  color_print "$cyan" "Downloading $dump_name ..."

  # Ansible is not a good solution for downloading large files.
  # The `fetch` module always hashes the file on remote, even with "validate_checksum: no", and shows no progress.
  # Next alternative is `scp`, but it's uncomfortable to build parameters with `ansible-ssh`...
  # So use ssh as scp, showing progress with `pv`.

  remote_dump_path="$(yq -r .project_name group_vars/all.yml)/db_dumps/$dump_name"

  ansible-ssh "$target" "pv -f \"$remote_dump_path\"" > $LOCAL_DUMPS_PATH/__tmp__.dump
  # Download to temp file to avoid storing a partial file with the same name,
  # and not downloading again if previous download is interrupted
  mv $LOCAL_DUMPS_PATH/__tmp__.dump "$local_dump_path"
fi

color_print "$cyan" "Restoring $dump_name ..."

# Delete and create DB before pg_restore because --clean "(drops) database objects before recreating them",
# so it leaves association tables that conflict with migrations. Also, --create has problems with the DB name.

psql \
  -c "drop database if exists \"$PGDATABASE\";" \
  -c "create database \"$PGDATABASE\";" \
  postgres

pg_restore --dbname="$PGDATABASE" --no-owner --no-acl --jobs="$(nproc)" "$local_dump_path"

color_print "$green" "Done"

migrations_check=0
dj migrate --check >/dev/null || migrations_check=$?

if (( migrations_check > 0 )); then
  color_print "$yellow" "There are unapplied migrations."
fi

# Note: it's possible that the DB now contains extra migrations
# (those present in django_migrations table, and schema, but not in code),
# but this is not automatically detected.
