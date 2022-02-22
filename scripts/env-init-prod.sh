#!/bin/bash
set -e
source scripts/utils.sh

env_file='.deploy.env'

cp "docker/.env.example" "$env_file"

postgres_db="project-name"  # TODO: also add $limit

color_print "$cyan" "Postgres database location?"

select db_loc in Local Remote; do
  if [[ "$db_loc" == "Local" ]]; then
    postgres_host="postgres"
    postgres_port="5432"
    postgres_user="postgres"
    postgres_password=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20)
    break

  elif [[ "$db_loc" == "Remote" ]]; then
    prompt "Postgres host?" "myproject.asdf.us-east-1.rds.amazonaws.com"
    postgres_host=$input

    prompt "Postgres port? (Note that DigitalOcean defaults to 25060)" "5432"
    postgres_port=$input

    prompt "Postgres user?" "postgres"
    postgres_user=$input

    prompt "Postgres password?" "asdf1234"
    postgres_password=$input

    prompt "Database name?" "$postgres_db"
    postgres_db=$input

    break
  fi
done

secret_key=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20)

django_debug=False

# Replace placeholders from template env file
sed -i "s|{{postgres_host}}|$postgres_host|g" $env_file
sed -i "s|{{postgres_port}}|$postgres_port|g" $env_file
sed -i "s|{{postgres_user}}|$postgres_user|g" $env_file
sed -i "s|{{postgres_password}}|$postgres_password|g" $env_file
sed -i "s|{{postgres_db}}|$postgres_db|g" $env_file
sed -i "s|{{secret_key}}|$secret_key|g" $env_file
sed -i "s|{{django_debug}}|$django_debug|g" $env_file
