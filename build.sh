#!/usr/bin/env bash

GIT_REF=$(git describe --match=NeVeRmAtCh --tags --always --abbrev --dirty)
BUILD_TIME=$(date --iso-8601=seconds)

docker-compose build --build-arg GIT_REF="$GIT_REF" --build-arg BUILD_TIME="$BUILD_TIME"
