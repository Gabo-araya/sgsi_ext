#!/bin/bash
set -euo pipefail

# Don't use the installer, which requires git, and installs whatever is at master branch.

FULL_COMMIT=115cee17015e4b5665e16dc4fd15c53e06a22f9a

cd ~
curl -fsSL https://github.com/ohmyzsh/ohmyzsh/archive/$FULL_COMMIT.tar.gz | tar xz
mv ohmyzsh-$FULL_COMMIT .oh-my-zsh

ln -s /usr/src/app/docker/zsh_prod/prod.zshrc .zshrc
ln -s /usr/src/app/docker/zsh_prod/production.zsh-theme .oh-my-zsh/custom/themes/
