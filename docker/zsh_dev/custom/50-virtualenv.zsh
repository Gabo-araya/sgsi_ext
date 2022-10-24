# Poetry's virtualenv should always be active because of VIRTUAL_ENV and PATH set in ".env".

# Check that VIRTUAL_ENV at least exists:
if ! [[ -d "$VIRTUAL_ENV" ]]; then
  echo "$fg[red]VIRTUAL_ENV is set to [$VIRTUAL_ENV], but it doesn't exist.
To fix it, run:
  env --unset=VIRTUAL_ENV poetry env use /usr/local/bin/python3
and in your .env, change VIRTUAL_ENV to the path printed by that command.
Then recreate the container.$reset_color"
fi

# However, this auto-activation makes "deactivate" unavailable.
# It could be manually implemented but it's not worth it.
deactivate() {
  echo 'Not implemented. Run "unset VIRTUAL_ENV" and manually edit PATH.'
  false
}
