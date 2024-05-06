#!/bin/bash
set -euxo pipefail

for target in $(yq --raw-output ".all.hosts | to_entries[] | select(.value.branch == \"$BRANCH_NAME\") | .key" ansible/inventory.yml); do
  host_ssh_key=$(yq --raw-output ".all.hosts.\"$target\".ansible_host + \" \" + .all.hosts.\"$target\".host_ssh_key" ansible/inventory.yml)
  echo "Adding host key for $target"
  echo "$host_ssh_key" >> ~/.ssh/known_hosts
done
