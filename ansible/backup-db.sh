#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if (( $# == 0 )); then
  echo "Please specify target server"
  exit 1
fi
limit=$1

ansible-playbook --limit "$limit" playbooks/backup-db.yml
