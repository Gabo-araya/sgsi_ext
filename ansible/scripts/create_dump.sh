# shellcheck shell=bash

color_print "$cyan" "Creating a new backup..."

# Horrible way of showing nice output and getting the db_dump with the same command.
# It's extracted from:
#
#   TASK [backup-db : set dump_name]
#   ok: [playg] => {
#       "ansible_facts": {
#           "dump_name": "playg-2022-02-14_22-49-05.dump"
#       },

dump_name=$(\
  ANSIBLE_FORCE_COLOR=True ansible-playbook -v --limit "$create_dump_limit" playbooks/backup-db.yml \
    | tee /dev/tty \
    | grep -Po '"dump_name": "\K.+\.dump(?=")')
