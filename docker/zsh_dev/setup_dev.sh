#!/bin/bash
set -euo pipefail

# This script sets up oh-my-zsh and customizations, at build-time (Dockerfile).

# Base installation:
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Customization:
ln -s /usr/src/app/docker/zsh_dev/load-devcontainer-customs.zsh $HOME/.oh-my-zsh/custom/
ln -s /usr/src/app/docker/zsh_dev/custom/ $HOME/.oh-my-zsh/custom/project
# $HOME/.oh-my-zsh/custom/shared will be bind-mounted by compose.

# Theme:
ln -s /usr/src/app/docker/zsh_dev/robbyrussell-poetryenv.zsh-theme $HOME/.oh-my-zsh/custom/themes/
sed -i 's/ZSH_THEME=".*"/ZSH_THEME="robbyrussell-poetryenv"/' $HOME/.zshrc

# History:
# Use history file inside separate folder, because while the file is being updated,
# a .LOCK is created next to it (so it's not enough to bind-mount the file).
# Sharing history with host is complicated (write to host ~/.zsh_history{,.LOCK} only for isolation,
# maybe preventing root ownership) but at least we can keep it and share it between containers.
# Prepend: (1i: insert before line 1)
sed -i '1i HISTFILE=$HOME/.oh-my-zsh/custom/shared/.zsh_history' $HOME/.zshrc
