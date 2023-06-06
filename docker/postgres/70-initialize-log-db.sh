#!/usr/bin/env bash
set -e
# This var makes psql fail to connect over unix socket, so unset it.
unset PGHOST

echo "Initializing log database"
psql --set db="$PGDATABASE-logs" <<EOSQL
CREATE DATABASE :"db";
EOSQL
