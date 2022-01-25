#!/bin/bash

# Format helpers for color_print
green="\033[0;32m"
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
