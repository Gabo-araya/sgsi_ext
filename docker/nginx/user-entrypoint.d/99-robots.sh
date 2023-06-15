#!/bin/sh

# If not declared, assume robots should be sent
if [ -z "$ENVIRONMENT_NAME" ]; then
  echo "\$ENVIRONMENT_NAME not set, assuming staging!"
  export ENVIRONMENT_NAME="staging"
fi

if [ "$ENVIRONMENT_NAME" != "production" ]; then
  export ADD_ROBOTS_HEADER='add_header X-Robots-Tag "noindex,nofollow,nosnippet,noarchive";'
  export ROBOTS_FILE=robots-staging.txt
else
  export ADD_ROBOTS_HEADER=''
  export ROBOTS_FILE=robots-prod.txt
fi

DEFINED_ENVS="\$ADD_ROBOTS_HEADER \$ROBOTS_FILE"
CONF_FILE=/etc/nginx/conf.d/app.conf
envsubst "$DEFINED_ENVS" < "$CONF_FILE" > "$CONF_FILE.new"
mv "$CONF_FILE.new" "$CONF_FILE"
