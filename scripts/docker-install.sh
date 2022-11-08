#!/bin/bash
set -e
cd "$(dirname "$0")"/..
source scripts/utils.sh
assert_outside_container

title_print "Installing Docker..."
# Check if docker is already installed
if [[ $(which docker) && $(docker --version) ]]; then
  color_print $green "Skipped! $(docker --version) found."
else
  # Download and install
  sudo apt-get install -y curl
  curl -fsSL https://get.docker.com -o get-docker.sh
  chmod +x get-docker.sh
  sudo ./get-docker.sh
  rm get-docker.sh

  color_print $green "Docker installation completed."
fi

# Check if we are allowed to manage docker as a non-root
if ! groups | grep -qw docker; then
  sudo groupadd docker &>/dev/null || true
  sudo usermod -aG docker "$USER"
  echo "Please reboot your computer to use Docker without sudo." >> quickstart-messages.log
fi

title_print "Installing Docker-compose..."
# Check if docker-compose is already installed
if [[ $(which docker-compose) && $(docker-compose --version) ]]; then
  color_print $green "Skipped! $(docker-compose --version) found."
else
  # Download and allow execute
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose

  color_print $green "Docker-compose installation completed."
fi

# Enable BuildKit
if ! [ -s /etc/docker/daemon.json ]; then
  # Default state (no file (or empty)), so create it:
  echo '{
  "features": {
    "buildkit": true
  }
}' | sudo tee /etc/docker/daemon.json >/dev/null

  sudo systemctl restart docker.service

  color_print $green "BuildKit has been enabled."

elif grep -q '"buildkit":\s*true' /etc/docker/daemon.json; then
  color_print $green "BuildKit already enabled."
  # Note: it's possible that even though the file contains buildkit:true,
  # a restart of the daemon is pending.

else
  color_print $yellow 'BuildKit appears not to be enabled.
  To enable it, set:
{
  "features": {
    "buildkit": true
  }
}
  in your /etc/docker/daemon.json file,
  and then restart the daemon with:
sudo systemctl restart docker.service'
fi
