#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if (( $# == 0 )); then
  echo "Please specify target server"
  exit 1
else
  limit=$1
fi

ansible-playbook --limit "$limit" playbooks/backup-db.yml
