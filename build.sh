#!/usr/bin/env bash

GIT_COMMIT=$(git describe --match=NeVeRmAtCh --always --abbrev --dirty)
BUILD_TIME=$(date --iso-8601=seconds)

docker-compose build --build-arg GIT_COMMIT="$GIT_COMMIT" --build-arg BUILD_TIME="$BUILD_TIME"
