#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
source ../scripts/utils.sh
should_be_inside_container

if (( $# == 0 )); then
  echo "Please specify target server"
  exit 1
fi
target=$1

ansible-playbook --limit "$target" playbooks/backup-db.yml
