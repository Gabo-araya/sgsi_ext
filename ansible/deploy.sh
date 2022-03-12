#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

deploy_recreate=0

while getopts rc opt; do
  case $opt in
    r)
      deploy_recreate=1
      ;;
    c)
      deploy_cache_ignore=1
      ;;
    ?)
      exit 1
  esac
done

export deploy_recreate
export deploy_cache_ignore
shift $((OPTIND - 1))

if (( $# == 0 )); then
  echo "Please specify target server"
  exit 1
fi
limit=$1
# improvement: implement update for two servers at same time

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
    (umask 177; scripts/env-init-prod.sh "$limit")
    cd ansible
    # shellcheck disable=SC2064  # Expand $limit now
    trap "rm -f ../deploy.$limit.env" EXIT  # Avoid keeping plaintext secrets outside server
    export create_dotenv=1
  else
    export create_dotenv=0
  fi
fi

# shellcheck disable=SC2086
ansible-playbook --limit "$limit" $tags playbooks/deploy.yml

if [[ "$(basename "$0")" != "update.sh" ]]; then
  : # TODO: "./manage.py createsuperuser" if none exists
fi
