#!/bin/sh

# If not declared, assume robots should be sent
if [ -z "$ALLOW_ROBOTS" ]; then
  echo "\$NO_ROBOTS not set, assuming development or staging!"
  export ALLOW_ROBOTS=0
fi

if [ "$ALLOW_ROBOTS" -eq 0 ]; then
  export ADD_ROBOTS_HEADER='add_header X-Robots-Tag "noindex,nofollow";'
  export ROBOTS_FILE=robots-staging.txt
else
  export ADD_ROBOTS_HEADER=''
  export ROBOTS_FILE=robots-prod.txt
fi

DEFINED_ENVS="\$ADD_ROBOTS_HEADER \$ROBOTS_FILE"
CONF_FILE=/etc/nginx/conf.d/app.conf
envsubst "$DEFINED_ENVS" < "$CONF_FILE" > "$CONF_FILE.new"
mv "$CONF_FILE.new" "$CONF_FILE"
