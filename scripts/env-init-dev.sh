#!/bin/bash
set -e
cd "$(dirname "$0")"/..
source scripts/utils.sh
assert_outside_container

env_file='.env'

# Create a new env file if it does not exist
if [ -f "$env_file" ]; then
  echo "Using existing $env_file"
else
  cp "docker/.env.example" "$env_file"

  # For servers, project_name has to be stable, so it's commited in group_vars/all.yml
  # and parsed with ansible or yq inside contaier.
  # But this script runs outside container, so no ansible or yq, and stability is not important,
  # and if user cloned repo to a folder with different name it could be more recognizable with
  # that name, so use project folder name:
  project_name=$(basename "$(dirname "$(dirname "$(realpath "$0")")")")

  # Assume defaults
  postgres_host="localhost"
  postgres_port="5432"
  postgres_user="postgres"
  postgres_password=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20)
  postgres_db=$project_name
  secret_key=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 50)
  django_debug=True
  aws_access_key_id=
  aws_secret_access_key=
  bucket_name=
  do_spaces_region=

  # Replace placeholders from template env file
  sed -i "s|{{postgres_host}}|$postgres_host|g" $env_file
  sed -i "s|{{postgres_port}}|$postgres_port|g" $env_file
  sed -i "s|{{postgres_user}}|$postgres_user|g" $env_file
  sed -i "s|{{postgres_password}}|$postgres_password|g" $env_file
  sed -i "s|{{postgres_db}}|$postgres_db|g" $env_file
  sed -i "s|{{secret_key}}|$secret_key|g" $env_file
  sed -i "s|{{django_debug}}|$django_debug|g" $env_file
  sed -i "s|{{aws_access_key_id}}|$aws_access_key_id|g" $env_file
  sed -i "s|{{aws_secret_access_key}}|$aws_secret_access_key|g" $env_file
  sed -i "s|{{bucket_name}}|$bucket_name|g" $env_file
  sed -i "s|{{do_spaces_region}}|$do_spaces_region|g" $env_file

  echo "Created $env_file file"
fi
