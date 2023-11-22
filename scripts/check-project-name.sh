#!/usr/bin/env bash
set -euo pipefail
source scripts/utils.sh

# Warn users about improperly configured projects. This includes:
# - Poetry project name
# - Node project name
# - Ansible project name
# - Jenkins PROJECT_REPONAME

failure=0
placeholder_name="project-name-placeholder"

# Safeguard for DPT development
if [[ -n "${SKIP_PROJECT_NAME_CHECK-}" ]]; then
  color_print $yellow "Skipping project name check."
  return 0
fi

# poetry
if ! command -v poetry >> /dev/null; then
  color_print $red "Poetry not found."
  return 1
fi

poetry_project_name=$(poetry version | awk \{'print $1'\})
if [ "$poetry_project_name" == "$placeholder_name" ]; then
  color_print $red "Found \"$poetry_project_name\" as the Poetry project name.
This project name should not be used for real projects.
Please update your pyproject.toml file and try again."
  failure=1
fi

# node
if ! command -v npm >> /dev/null; then
  color_print $red "npm not found."
  return 1
fi

node_project_name=$(npm run env | grep "npm_package_name" | cut -d "=" -f 2)
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
