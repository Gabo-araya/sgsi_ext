#!/bin/bash
set -e
source scripts/utils.sh

env_file='.env'

# Create a new env file if it does not exist
title_print "Checking .env files..."
if [ -f "$env_file" ]; then
  echo "Using existing .env"
else
  echo "Creating .env file..."
  cp "docker/.env.example" "$env_file"

  # Prompt for inputs
  prompt "Postgres host?" "localhost"
  postgres_host=$input

  prompt "Postgres user?" "postgres"
  postgres_user=$input

  postgres_password=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20)
  prompt "Postgres password?" "$postgres_password"
  postgres_password=$input

  prompt "Database name?" "project-name"
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

fi
color_print $green 'Done'
