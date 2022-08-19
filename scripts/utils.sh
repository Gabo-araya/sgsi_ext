# shellcheck shell=bash

# Format helpers for color_print
green="\033[0;32m"
blue="\033[0;34m"
cyan="\033[0;36m"
yellow="\033[0;33m"
red="\033[0;31m"
default="\033[0m"

function color_print() {
  local color=$1
  local message=$2

  echo -e "${color}${message}${default}\n"
}

function title_print() {
  local message=$1

  echo -e "\n\033[44;1;37m ▸ ${message} ${default}\n"
  sleep 1
}

function prompt() {
  local prompt_message=$1
  local default_value=$2

  echo -n -e "$cyan$prompt_message$default"
  read -r -p" [$default_value]: " input
  input=${input:-$default_value}
}

function random_chars() {
  local count=$1

  chars=$(tr -dc A-Za-z0-9 </dev/urandom | head -c $count)
}

function assert_outside_container() {
  if [[ -n "${RUNNING_IN_CONTAINER-}" ]]; then
    color_print $red "This script must be run out of the container"
    exit 1
  fi
}

function should_be_inside_container() {
  if [[ -z "${RUNNING_IN_CONTAINER-}" ]]; then
    color_print $red "This script is intended to be run inside the container"
    # Add "RUNNING_IN_CONTAINER=x" to your env vars to skip this check, if you are working without docker
    exit 1
  fi
}

# TODO: after merging all PRs, check that all `find . -not -path "./docker/*" -name "*.sh" -executable` handle inside/outside container
