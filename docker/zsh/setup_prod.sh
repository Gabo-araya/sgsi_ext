#!/bin/bash
set -euo pipefail

# Don't use the installer, which requires git, and installs whatever is at master branch.

FULL_COMMIT=53863e7b3ff0c2e2816e90dab3d870adebdf49c7

cd ~
curl -fsSL https://github.com/ohmyzsh/ohmyzsh/archive/$FULL_COMMIT.tar.gz | tar xz
mv ohmyzsh-$FULL_COMMIT .oh-my-zsh

ln -s /usr/src/app/docker/zsh/production.zshrc .zshrc
ln -s /usr/src/app/docker/zsh/production.zsh-theme .oh-my-zsh/custom/themes/
