#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if (( $# == 0 )); then
  echo "Please specify target server"
  exit 1
fi
limit=$1

if [[ $# -gt 1 && $2 == '--recreate' ]]; then
  export recreate=1
  echo "Will recreate containers."
fi

if [[ "$(basename "$0")" == "update.sh" ]]; then
  tags="--tags update"
else
  tags=""

  echo "Checking for .env existance on $limit..."

  stat_ansible_res=0
  stat_json=$(ANSIBLE_STDOUT_CALLBACK=json ansible-playbook -l "$limit" playbooks/stat_dotenv.yml) || stat_ansible_res=$?
  if (( stat_ansible_res > 0 )); then
    echo "$stat_json" | jq
    exit $stat_ansible_res
  fi

  stat_jq_res=0
  echo "$stat_json" | jq --exit-status '.plays[0].tasks[0].hosts[].stat.exists' >/dev/null || stat_jq_res=$?
  if (( stat_jq_res > 1 )); then
    exit $stat_jq_res

  elif (( stat_jq_res == 1 )); then
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
ansible-playbook --limit "$limit" $tags playbooks/deploy.yml

if [[ "$(basename "$0")" != "update.sh" ]]; then
  : # TODO: "./manage.py createsuperuser" if none exists
  # https://raw.githubusercontent.com/selivan/ansible-ssh/892c48c828ee0f56d897706009096327076429f9/ansible-ssh
fi
