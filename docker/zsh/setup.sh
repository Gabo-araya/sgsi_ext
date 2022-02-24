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
ln -s /usr/src/app/docker/zsh/robbyrussell-poetryenv.zsh-theme  /root/.oh-my-zsh/custom/themes/
sed -i 's/ZSH_THEME=".*"/ZSH_THEME="robbyrussell-poetryenv"/' /root/.zshrc
