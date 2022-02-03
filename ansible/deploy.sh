#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if (( $# == 0 )); then
  echo "Please specify limit"
  exit 1
else
  limit=$1
fi

echo "Checking for .env existance on $limit..."
stat_dotenv_json=$(ANSIBLE_STDOUT_CALLBACK=json ansible-playbook -l "$limit" utils/stat_dotenv.yml)
stat_dotenv_res=0
echo "$stat_dotenv_json" | jq --exit-status '.plays[0].tasks[0].hosts[].stat.exists' >/dev/null || stat_dotenv_res=$?

if (( stat_dotenv_res > 1 )); then
  exit $stat_dotenv_res
elif (( stat_dotenv_res == 1 )); then
  # Prompt for new .env file
  cd ..
  (umask 177; scripts/env-init.sh .deploy.env)
  sed -i 's/DEBUG=True/DEBUG=False/' .deploy.env
  cd ansible
  trap "rm ../.deploy.env" EXIT
  export create_dotenv=1
else
  export create_dotenv=0
fi

ansible-playbook --limit "$limit" deploy.yml
