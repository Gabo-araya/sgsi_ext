#!/bin/bash
set -e
source scripts/utils.sh

if (( $# == 0 )); then
  echo "No limit"
  exit 1
fi

limit=$1
env_file="deploy.$limit.env"

cp "docker/.env.example" "$env_file"

project_name=$(yq -r .project_name ansible/group_vars/all.yml)
postgres_db=$project_name-$limit

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

color_print "$cyan" "Files storage location?"

select files_loc in Local "Amazon S3" "DigitalOcean Spaces"; do
  if [[ "$files_loc" == "Local" ]]; then
    aws_access_key_id=
    aws_secret_access_key=
    bucket_name=
    do_spaces_region=
    break

  elif [[ "$files_loc" == "Amazon S3" ]]; then
    prompt "AWS_ACCESS_KEY_ID?" "AKIA..."
    aws_access_key_id=$input

    prompt "AWS_SECRET_ACCESS_KEY?" "s..."
    aws_secret_access_key=$input

    prompt "Bucket name?" "bucket-name"
    bucket_name=$input

    do_spaces_region=
    break

  elif [[ "$files_loc" == "DigitalOcean Spaces" ]]; then
    prompt "AWS_ACCESS_KEY_ID?" "AKIA..."
    aws_access_key_id=$input

    prompt "AWS_SECRET_ACCESS_KEY?" "s..."
    aws_secret_access_key=$input

    prompt "Bucket name?" "bucket-name"
    bucket_name=$input

    prompt "Region?" "nyc3"
    do_spaces_region=$input
    break
  fi
done

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
