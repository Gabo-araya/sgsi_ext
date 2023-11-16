#!/bin/bash
set -e
cd "$(dirname "$0")"
source scripts/utils.sh
should_be_inside_container

function makemessages {
  if [[ -d "$1" ]]; then
    cd "$1"
    mkdir -p locale/es

    if [[ "$1" == "assets" ]]; then
      django-admin makemessages --add-location file -d djangojs -l es -e js,jsx,ts,tsx
    else
      django-admin makemessages --add-location file -l es -e pug,html,txt,py
    fi

    cd ..
  else
    color_print $red "folder \"$1\" does not exist"
  fi
}

function translate {
  color_print $green "translating \"$1\""
  if $COMPILE; then
    cd "$1"
    django-admin compilemessages
    cd ..
  else
    makemessages "$1"
  fi
}

function translate_all {
  TARGET_APPS=(
    api_client
    base
    messaging
    parameters
    regions
    users
  )
  ./manage.py check_translate_apps "${TARGET_APPS[@]}"

  for app in "${TARGET_APPS[@]}"; do
    translate "$app"
  done
}

COMPILE=false

while getopts "c" OPTION; do
  case $OPTION in
    c)
      color_print $blue "Compiling"
      COMPILE=true
      ;;
    ?)
      exit 1
      ;;
  esac
done

if [[ "$1" ]] && [[ $1 != '-c' ]] ; then
  color_print $blue "Only on app \"$1\""
  translate "$1"
elif [[ "$2" ]] && [[ $2 != '-c' ]] ; then
  color_print $blue "Only on app \"$2\""
  translate "$2"
else
  translate_all
fi
