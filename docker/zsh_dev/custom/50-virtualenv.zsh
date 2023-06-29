# Poetry's virtualenv should always be active because of DEV_VIRTUAL_ENV and DEV_PATH set in ".env".
# (mapped to VIRTUAL_ENV and PATH, respectively)

RECREATE_FIX_MSG="To fix it, run:
  env --unset=VIRTUAL_ENV poetry env use /usr/local/bin/python3
and in your .env, change DEV_VIRTUAL_ENV to the path printed by that command.
Then recreate the container:
  - vscode devcontainer: F1 --> Rebuild Container
  - compose: docker compose up -d --force-recreate"

# Check that VIRTUAL_ENV exists:
if ! [[ -d "$VIRTUAL_ENV" ]]; then
  echo "$fg[red]VIRTUAL_ENV is set to [$VIRTUAL_ENV], but it doesn't exist.
$RECREATE_FIX_MSG$reset_color"

else  # Check that VIRTUAL_ENV matches project-name
  poetry_path=$(poetry env info --path)       # This command fails if there's no virtualenv with name from pyproject.toml ($VIRTUAL_ENV has other name)
  if (( $? > 0 )) \
    || [[ "$poetry_path" != "$VIRTUAL_ENV" ]] # These vars are different if both virtualenvs exist, but $VIRTUAL_ENV points to the wrong one
  then
    echo "$fg[red]\$VIRTUAL_ENV and name from pyproject.toml are inconsistent.
$RECREATE_FIX_MSG$reset_color"
  fi
fi

unset poetry_path RECREATE_FIX_MSG


# However, this auto-activation makes "deactivate" unavailable.
# It could be manually implemented but it's not worth it.
deactivate() {
  echo 'Not implemented. Run "unset VIRTUAL_ENV" and manually edit PATH.'
  false
}
