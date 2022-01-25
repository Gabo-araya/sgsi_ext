#!/bin/bash
set -e
source scripts/utils.sh

title_print "Installing Docker..."
if [[ $(which docker) && $(docker --version) ]]; then
  color_print $green "Skipped! $(docker --version) found."
else
  curl -fsSL https://get.docker.com -o get-docker.sh
  chmod +x get-docker.sh
  ./get-docker.sh
  rm get-docker.sh
  color_print $green "Docker installation completed"
fi

title_print "Installing Docker-compose..."
if [[ $(which docker-compose) && $(docker-compose --version) ]]; then
  color_print $green "Skipped! $(docker-compose --version) found."
else
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  color_print $green "Docker-compose installation completed"
fi
