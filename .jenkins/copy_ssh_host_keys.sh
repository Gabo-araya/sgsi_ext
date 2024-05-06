#!/bin/bash
set -euo pipefail

if (( $# == 0 )); then
  echo "Usage: $0 <inventory_entry>"
  exit 1
fi
target=$1

host_ssh_key=$(yq --raw-output ".all.hosts.\"$target\".ansible_host + \" \" + .all.hosts.\"$target\".host_ssh_key" ansible/inventory.yml)
host_ssh_key="${host_ssh_key%%*[[:space:]]}"

if [[ -z "$host_ssh_key" ]]; then
  echo "No host keys found for target $target"
  exit 1
fi

echo "Adding host key for $target"
echo "$host_ssh_key" >> ~/.ssh/known_hosts
