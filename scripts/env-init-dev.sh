#!/bin/bash
set -e
source scripts/utils.sh

env_file='.env'

# Create a new env file if it does not exist
if [ -f "$env_file" ]; then
  echo "Using existing $env_file"
else
  cp "docker/.env.example" "$env_file"

  # Assume defaults
  postgres_host="localhost"
  postgres_port="5432"
  postgres_user="postgres"
  postgres_password=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20)
  postgres_db="project-name"  # TODO (yq? grep+cut? dirname+basename?)
  secret_key=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20)
  django_debug=True

  # Replace placeholders from template env file
  sed -i "s|{{postgres_host}}|$postgres_host|g" $env_file
  sed -i "s|{{postgres_port}}|$postgres_port|g" $env_file
  sed -i "s|{{postgres_user}}|$postgres_user|g" $env_file
  sed -i "s|{{postgres_password}}|$postgres_password|g" $env_file
  sed -i "s|{{postgres_db}}|$postgres_db|g" $env_file
  sed -i "s|{{secret_key}}|$secret_key|g" $env_file
  sed -i "s|{{django_debug}}|$django_debug|g" $env_file

  echo "Created $env_file file"
fi
