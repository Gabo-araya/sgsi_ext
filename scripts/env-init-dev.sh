#!/usr/bin/env bash
set -eu
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
  project_name=$(set -o pipefail; grep -E "^project_name: " ansible/group_vars/all.yml | cut -d' ' -f2)

  who=$(whoami)

if [[ "$OSTYPE" == darwin* ]]; then
  echo "NOTE: on macOS system your password might be required to get current timezone."
  tz=$(sudo systemsetup -gettimezone | awk -F: '{tz=$2; sub(/^ */, "", tz); print tz; exit}')
  host_uid=2640
  host_gid=2640
else
  tz=$(cat /etc/timezone)
  host_uid=$(id -u)
  host_gid=$(id -g)
fi

  # Not yet known, leave as is to be set later:
  virtual_env="{{virtual_env}}"

  # Assume defaults
  postgres_host="localhost"
  postgres_port="15432"
  postgres_user="postgres"
  postgres_password=$(perl -pe 'binmode(STDIN, ":bytes"); tr/A-Za-z0-9//dc;' < /dev/urandom | head -c 20)
  postgres_db=$project_name
  secret_key=$(perl -pe 'binmode(STDIN, ":bytes"); tr/A-Za-z0-9//dc;' < /dev/urandom | head -c 50)
  django_debug=True
  environment_name=Development
  enable_debug_toolbar=True
  enable_django_extensions=True
  aws_access_key_id=
  aws_secret_access_key=
  bucket_name=
  do_spaces_region=
  redis_cache_url=
  celery_broker_url=
  celery_result_backend=
  xff_trusted_proxy_depth=1

  # Replace placeholders from template env file
  perl -pi -e "s|{{who}}|$who|g" $env_file
  perl -pi -e "s|{{host_uid}}|$host_uid|g" $env_file
  perl -pi -e "s|{{host_gid}}|$host_gid|g" $env_file
  perl -pi -e "s|{{tz}}|$tz|g" $env_file
  perl -pi -e "s|{{virtual_env}}|$virtual_env|g" $env_file
  perl -pi -e "s|{{postgres_host}}|$postgres_host|g" $env_file
  perl -pi -e "s|{{postgres_port}}|$postgres_port|g" $env_file
  perl -pi -e "s|{{postgres_user}}|$postgres_user|g" $env_file
  perl -pi -e "s|{{postgres_password}}|$postgres_password|g" $env_file
  perl -pi -e "s|{{postgres_db}}|$postgres_db|g" $env_file
  perl -pi -e "s|{{secret_key}}|$secret_key|g" $env_file
  perl -pi -e "s|{{django_debug}}|$django_debug|g" $env_file
  perl -pi -e "s|{{redis_cache_url}}|$redis_cache_url|g" $env_file
  perl -pi -e "s|{{celery_broker_url}}|$celery_broker_url|g" $env_file
  perl -pi -e "s|{{celery_result_backend}}|$celery_result_backend|g" $env_file
  perl -pi -e "s|{{environment_name}}|$environment_name|g" $env_file
  perl -pi -e "s|{{enable_debug_toolbar}}|$enable_debug_toolbar|g" $env_file
  perl -pi -e "s|{{enable_django_extensions}}|$enable_django_extensions|g" $env_file
  perl -pi -e "s|{{aws_access_key_id}}|$aws_access_key_id|g" $env_file
  perl -pi -e "s|{{aws_secret_access_key}}|$aws_secret_access_key|g" $env_file
  perl -pi -e "s|{{bucket_name}}|$bucket_name|g" $env_file
  perl -pi -e "s|{{do_spaces_region}}|$do_spaces_region|g" $env_file
  perl -pi -e "s|{{xff_trusted_proxy_depth}}|$xff_trusted_proxy_depth|g" $env_file

  echo "Created $env_file file"
fi
