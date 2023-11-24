#!/usr/bin/env bash
set -euo pipefail
source scripts/utils.sh

# Warn users about improperly configured projects. This includes:
# - Poetry project name
# - Node project name
# - Ansible project name
# - Jenkins PROJECT_REPONAME

failure=0
# obfuscate so sed or perl can't mess with the check
placeholder_name=$(echo "70726f6a6563742d6e616d652d706c616365686f6c646572" | xxd -r -p)

# Safeguard for DPT development
if [[ -n "${SKIP_PROJECT_NAME_CHECK-}" ]]; then
  color_print $yellow "Skipping project name check."
  return 0
fi

# poetry
poetry_project_name=$(grep "name" pyproject.toml | cut -d "=" -f 2 | tr -d "'\" ")
if [ "$poetry_project_name" == "$placeholder_name" ]; then
  color_print $red "Found \"$poetry_project_name\" as the Poetry project name.
This project name should not be used for real projects.
Please update your pyproject.toml file and try again."
  failure=1
fi

# node
node_project_name=$(grep "name" package.json | cut -d ":" -f 2 | tr -d '", ')
if [ "$node_project_name" == "$placeholder_name" ]; then
  color_print $red "Found \"$node_project_name\" as the npm project name.
This project name should not be used for real projects.
Please update your package.json file and try again."
  failure=1
fi

# ansible project name
ansible_project_name=$(grep "project_name" ansible/group_vars/all.yml | awk \{'print $2'\})
if [ "$ansible_project_name" == "$placeholder_name" ]; then
  color_print $red "Found \"$ansible_project_name\" as the ansible project name.
This project name should not be used for real projects.
Please update ansible/group_vars/all.yml and try again."
  failure=1
fi

# Jenkins PROJECT_REPONAME
jenkins_project_name=$(grep "PROJECT_REPONAME =" Jenkinsfile | awk -F'=' \{'print $2'\} | tr -d "' ")
if [ "$jenkins_project_name" == "$placeholder_name" ]; then
  color_print $red "Found \"$jenkins_project_name\" as the Jenkins project name.
This project name should not be used for real projects.
Please update Jenkinsfile and try again."
  failure=1
fi

if [ $failure -ne 0 ]; then
  exit 1
fi
