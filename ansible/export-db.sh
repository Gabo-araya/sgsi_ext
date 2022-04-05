#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
source ../scripts/utils.sh
should_be_inside_container

if (( $# < 2 )); then
  echo "Usage: export-db.sh src dest [dump_name]"
  exit 1
fi
src=$1
dest=$2
dump_name=${3:-}

if [[ ! $dump_name ]]; then
  create_dump_limit=$src
  source scripts/create_dump.sh
fi

# Improvement: add support for https://github.com/Tesorio/django-anon

color_print "$cyan" "Transfering $dump_name ..."

dumps_path="$(yq -r .project_name group_vars/all.yml)/db_dumps"

# Improvement: direct copy:

# deploy.yml:
#      apt:
#        ...
#        - xz-utils      # For ansible apt deb
#
#    - name: install croc
#      apt:
#        deb: https://github.com/schollz/croc/releases/download/v9.5.1/croc_9.5.1_Linux-64bit.deb
#        state: present
#      become: yes

# code=$(head -c 16 /dev/urandom | xxd -p)
# croc --no-compress send --code=$code "$dumps_path/$dump_name"
# croc --out="$dumps_path" --yes --overwrite $code
# https://stackoverflow.com/questions/7197527/how-can-i-wait-for-certain-output-from-a-process-then-continue-in-bash/

# For now, copy through local pc like `scp -3`:
ansible-ssh "$src" "pv -f \"$dumps_path/$dump_name\"" \
  | ansible-ssh "$dest" "cat > \"$dumps_path/$dump_name\""

color_print "$cyan" "Restoring $dump_name ..."
ansible-playbook --limit "$dest" -e dump_name="$dump_name" playbooks/restore-dump.yml

color_print "$green" "Done"
