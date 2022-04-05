#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
source ../scripts/utils.sh
should_be_inside_container

while getopts rc opt; do
  case $opt in
    r)
      export deploy_recreate=1
      ;;
    c)
      export deploy_cache_ignore=1
      ;;
    ?)
      exit 1
  esac
done

shift $((OPTIND - 1))

if (( $# == 0 )); then
  echo "Please specify target server"
  exit 1
fi
target=$1


ansible-role() {
  ansible "$target" --playbook-dir playbooks/ -m include_role -a name="$1"
}


if [[ "$(basename "$0")" == "update.sh" ]]; then
  tags="--tags update"
else
  tags=""

  echo "Checking for .env existance on $target..."

  stat_ansible_rc=0
  stat_json=$(ANSIBLE_STDOUT_CALLBACK=json ansible-playbook -l "$target" playbooks/check-cloned.yml) || stat_ansible_rc=$?
  if (( stat_ansible_rc > 0 )); then
    echo "$stat_json" | jq
    exit $stat_ansible_rc
  fi

  cloned_jq_rc=0
  echo "$stat_json" | jq --exit-status '.plays[0].tasks[0].hosts[].stat.exists' >/dev/null || cloned_jq_rc=$?
  if (( cloned_jq_rc > 1 )); then
    exit $cloned_jq_rc
  fi

  env_jq_rc=0
  echo "$stat_json" | jq --exit-status '.plays[0].tasks[1].hosts[].stat.exists' >/dev/null || env_jq_rc=$?
  if (( env_jq_rc > 1 )); then
    exit $env_jq_rc
  fi

  if (( cloned_jq_rc == 1 )); then
    # Run git clone before asking .env questions, so they don't get lost.
    # It would have been better to mkdir in server and copy .env, and then clone,
    # but git fails with "not an empty directory".
    ansible-role git-clonepull
  fi

  if (( env_jq_rc == 1 )); then
    # Prompt for new .env file
    cd ..
    (umask 177; scripts/env-init-prod.sh "$target")
    cd ansible
    # shellcheck disable=SC2064  # Expand $target now
    trap "rm -f ../deploy.$target.env" EXIT  # Avoid keeping plaintext secrets outside server
    export create_dotenv=1
  else
    export create_dotenv=0
  fi
fi

# shellcheck disable=SC2086
ansible-playbook --limit "$target" $tags playbooks/deploy.yml

if [[ "$(basename "$0")" != "update.sh" ]]; then
  ansible-ssh "$target" -t "$(yq -r .project_name group_vars/all.yml)/ansible/scripts/offer_superuser.sh"
fi
