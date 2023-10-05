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

CONF_FILE=/etc/nginx/conf.d/app.conf
HARDENING_FILE=/etc/nginx/user_conf.d/z.hardening.conf
envsubst "\$ROBOTS_FILE" < "$CONF_FILE" > "$CONF_FILE.new"
envsubst "\$ADD_ROBOTS_HEADER" < "$HARDENING_FILE" > "$HARDENING_FILE.new"
mv "$CONF_FILE.new" "$CONF_FILE"
mv "$HARDENING_FILE.new" "$HARDENING_FILE"
