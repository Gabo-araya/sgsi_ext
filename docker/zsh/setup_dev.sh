#!/bin/bash
set -euo pipefail

# This script sets up oh-my-zsh and customizations, at build-time (Dockerfile).

# Base installation:
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Customization:
ln -s /usr/src/app/docker/zsh/load-devcontainer-customs.zsh /root/.oh-my-zsh/custom/
ln -s /usr/src/app/docker/zsh/custom/ /root/.oh-my-zsh/custom/project
# /root/.oh-my-zsh/custom/shared will be bind-mounted by compose.

# Theme:
ln -s /usr/src/app/docker/zsh/robbyrussell-poetryenv.zsh-theme /root/.oh-my-zsh/custom/themes/
sed -i 's/ZSH_THEME=".*"/ZSH_THEME="robbyrussell-poetryenv"/' /root/.zshrc

# History:
# Use history file inside separate folder, because while the file is being updated,
# a .LOCK is created next to it (so it's not enough to bind-mount the file).
# Sharing history with host is complicated (write to host ~/.zsh_history{,.LOCK} only for isolation,
# maybe preventing root ownership) but at least we can keep it and share it between containers.
# Prepend: (1i: insert before line 1)
sed -i '1i HISTFILE=/root/.oh-my-zsh/custom/shared/.zsh_history' /root/.zshrc
