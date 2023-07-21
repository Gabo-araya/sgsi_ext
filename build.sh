#!/usr/bin/env bash

GIT_REF=$(git describe --tags --always --abbrev --dirty)
BUILD_TIME=$(date --iso-8601=seconds)

docker compose build --build-arg GIT_REF="$GIT_REF" --build-arg BUILD_TIME="$BUILD_TIME"

# Sorry, no build-arg for PROJECT-NAME, as yq may not be available outside container.
