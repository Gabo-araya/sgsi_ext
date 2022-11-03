#!/bin/bash
set -euo pipefail
source scripts/utils.sh

if ! should_be_inside_container &>/dev/null; then
  # Attempt to make the message more visible with yellow and [tag], because npm prints too much text.
  color_print $yellow "[django3-project-template] Please use npm inside the container. This is to prevent potential incompatibilities across versions."
  exit 1
fi
