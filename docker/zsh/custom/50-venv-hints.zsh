# Poetry's virtualenv should always be active,
# because quickstart.sh sets VIRTUAL_ENV and PATH in .env
if [[ -n "$VIRTUAL_ENV" ]]; then
  # However, this makes "deactivate" unavailable.
  # It could be manually implemented but it's not worth it.
  deactivate() {
    echo 'Not implemented. Run "unset VIRTUAL_ENV" and manually edit PATH.'
    false
  }

else
  source "$(cd /usr/src/app && poetry env info --path)/bin/activate"
  echo "$fg[white]virtualenv was not active." \
    "Exit container and run ./quickstart.sh to have it enabled for \"docker-compose exec\"$reset_color"
fi
