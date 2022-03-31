#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"/..
source scripts/utils.sh
assert_outside_container

# If sudo fails, make it fail here instead of at next command, mixing return codes:
sudo --validate

lsof_rc=0
pid=$(sudo lsof -t -i:5432 | head -n1) || lsof_rc=$?

if (( lsof_rc > 0 )); then
  # lsof_rc == 1 --> port 5432 is clear
  # lsof_rc > 1  --> I don't know what to do, so exit anyway
  exit 0
fi

is_pid_running_in_docker() {
  grep -q docker "/proc/$1/cgroup"
}

if is_pid_running_in_docker "$pid"; then
  # It shouldn't be postgres from this project because quickstart.sh stops it.
  color_print "$red" "Port 5432 is in use by a Docker container"

  maybe_container_id=$(grep -Po ":/docker/\K.*" "/proc/$pid/cgroup" | head -n1) || true
  # ^ This fails if there's a container with the port published, but no process bound to it.

  if [[ -n "$maybe_container_id" ]]; then
    docker ps --filter "id=$maybe_container_id"
  else
    docker ps --filter expose=5432
    # ^ This fails for network=host
  fi
  # I think this covers all cases.

else
  color_print "$red" "Port 5432 is in use"

  is_from_postgres_systemd() {
    # "unit" is systemd unit (postgresql@14-main.service, user@1000.service, etc)
    # shellcheck disable=SC2009 # "unit" not available in pgrep
    ps -o unit --no-headers "$pid" | grep -qw postgresql
  }

  if is_from_postgres_systemd; then

cat <<EOF
You can stop the PostgreSQL running in your computer with:
    sudo systemctl stop postgresql
and later start it with:
    sudo systemctl start postgresql
To stop it and prevent starting automatically at boot:
    sudo systemctl disable --now postgresql
EOF

  # elif... brew? something else?
  else
    ps "$pid"
  fi
fi

exit 1
