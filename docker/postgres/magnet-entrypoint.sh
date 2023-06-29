#!/usr/bin/env bash

# This entrypoint is run before the original one,
# to handle the case where an external database is used,
# so this container should not create another database, to prevent confusion.
# But it should still work for pg_dump and other commands,
# without having to use extra flags as all config is set through .env

arg1="$1"
will_start_postgres_server() {
  [[ "$arg1" == "postgres" ]]
}

host_is_remote() {
  [[ "$PGHOST" != "localhost" && "$PGHOST" != "postgres" ]]
}

if will_start_postgres_server && host_is_remote; then
  echo
  echo "magnet-entrypoint: Not running postgres server, container will just sleep."
  echo
  # Sleep and stay running so postgresql-client commands can be run with "docker compose exec".

  # Fake the healthcheck:
  echo -e '#!/bin/sh'"\necho fake ok" > /usr/local/bin/pg_isready   # chmod not required
  # If PGHOST changes, the container has to be recreated anyway, so this change will be lost.

  # Signal handling stuff, so "stop" doesn't timeout at 10s:
  sleep inf &
  sleep_pid=$!
  trap 'kill $sleep_pid' SIGTERM SIGINT
  wait
  exit 0
fi

exec docker-entrypoint.sh "$@"
