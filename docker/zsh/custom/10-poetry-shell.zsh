export VIRTUAL_ENV_DISABLE_PROMPT=x

if [[ -n "$REMOTE_CONTAINERS" ]]; then
  : # Remote-Containers will source the virtualenv later
else
  source "$(cd /usr/src/app && poetry env info --path)/bin/activate"
fi
