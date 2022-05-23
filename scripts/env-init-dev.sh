#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"/..
source scripts/utils.sh
assert_outside_container

env_file='.env'

# Create a new env file if it does not exist
if [ -f "$env_file" ]; then
  echo "Using existing $env_file"
else
  cp "docker/.env.example" "$env_file"

  # As this script runs outside the container, yq may not be available to parse the file.
  # So just grep and cut. This is for development only so no servers are at risk.
  project_name=$(grep -E "^project_name: " ansible/group_vars/all.yml | cut -d' ' -f2)

  who=$(whoami)
  host_uid=$(id -u)
  host_gid=$(id -g)

  # Not yet known, leave as is to be set later:
  virtual_env=virtual_env

  # Assume defaults
  postgres_host="localhost"
  postgres_port="15432"
  postgres_user="postgres"
  postgres_password=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20)
  postgres_db=$project_name
  secret_key=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 50)
  django_debug=True
  is_critical_env=False
  aws_access_key_id=
  aws_secret_access_key=
  bucket_name=
  do_spaces_region=

  # Replace placeholders from template env file
  sed -i "s|{{who}}|$who|g" $env_file
  sed -i "s|{{host_uid}}|$host_uid|g" $env_file
  sed -i "s|{{host_gid}}|$host_gid|g" $env_file
  sed -i "s|{{virtual_env}}|$virtual_env|g" $env_file
  sed -i "s|{{postgres_host}}|$postgres_host|g" $env_file
  sed -i "s|{{postgres_port}}|$postgres_port|g" $env_file
  sed -i "s|{{postgres_user}}|$postgres_user|g" $env_file
  sed -i "s|{{postgres_password}}|$postgres_password|g" $env_file
  sed -i "s|{{postgres_db}}|$postgres_db|g" $env_file
  sed -i "s|{{secret_key}}|$secret_key|g" $env_file
  sed -i "s|{{django_debug}}|$django_debug|g" $env_file
  sed -i "s|{{is_critical_env}}|$is_critical_env|g" $env_file
  sed -i "s|{{aws_access_key_id}}|$aws_access_key_id|g" $env_file
  sed -i "s|{{aws_secret_access_key}}|$aws_secret_access_key|g" $env_file
  sed -i "s|{{bucket_name}}|$bucket_name|g" $env_file
  sed -i "s|{{do_spaces_region}}|$do_spaces_region|g" $env_file

  echo "Created $env_file file"
fi
