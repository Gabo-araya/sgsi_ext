#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if (( $# == 0 )); then
  echo "Please specify limit"
  exit 1
else
  limit=$1
fi

if [[ "$(basename "$0")" == "update.sh" ]]; then
  tags="--tags update"
else
  tags=""

  echo "Checking for .env existance on $limit..."
  stat_dotenv_json=$(ANSIBLE_STDOUT_CALLBACK=json ansible-playbook -l "$limit" utils/stat_dotenv.yml)
  stat_dotenv_res=0
  echo "$stat_dotenv_json" | jq --exit-status '.plays[0].tasks[0].hosts[].stat.exists' >/dev/null || stat_dotenv_res=$?

  if (( stat_dotenv_res > 1 )); then
    exit $stat_dotenv_res
  elif (( stat_dotenv_res == 1 )); then
    # Prompt for new .env file
    cd ..
    (umask 177; scripts/env-init-prod.sh .deploy.env)
    cd ansible
    trap "rm ../.deploy.env" EXIT
    export create_dotenv=1
  else
    export create_dotenv=0
  fi
fi

# shellcheck disable=SC2086
ansible-playbook --limit "$limit" $tags deploy.yml

if [[ "$(basename "$0")" != "update.sh" ]]; then
  : # TODO: "./manage.py createsuperuser" if none exists
  # https://raw.githubusercontent.com/selivan/ansible-ssh/892c48c828ee0f56d897706009096327076429f9/ansible-ssh
fi
