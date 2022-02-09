#!/bin/bash
set -e
source scripts/utils.sh

env_file='.deploy.env'

cp "docker/.env.example" "$env_file"

# Prompt for inputs
prompt "Postgres host?" "postgres"
postgres_host=$input

prompt "Postgres user?" "postgres"
postgres_user=$input

postgres_password=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20)
prompt "Postgres password?" "$postgres_password"
postgres_password=$input

prompt "Database name?" "project-name"  # TODO: project_name + limit
postgres_db=$input

secret_key=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20)
prompt "Secret key?" "$secret_key"
secret_key=$input

# Replace placeholders from template env file
sed -i "s|{{postgres_host}}|$postgres_host|g" $env_file
sed -i "s|{{postgres_user}}|$postgres_user|g" $env_file
sed -i "s|{{postgres_password}}|$postgres_password|g" $env_file
sed -i "s|{{postgres_db}}|$postgres_db|g" $env_file
sed -i "s|{{secret_key}}|$secret_key|g" $env_file
sed -i 's|DEBUG=True|DEBUG=False|' $env_file
