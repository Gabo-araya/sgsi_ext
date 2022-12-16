# Installs node_modules if not present.
#
# This can't be done in Dockerfile, because then the installed node_modules
# are shadowed by bind-mounting the project's folder.

_in_project_path() {
  # Do nothing if the terminal is not for the project, for example for a package in the virtualenv,
  # instead of failing with "ENOENT /home/user/.cache/pypoetry/virtualenvs/.../package.json"
  [[ "$PWD" == "/usr/src/app" ]]
}

_node_modules_present() {
  [[ -d node_modules ]]
}

_built_assets_present() {
  # If the javascript of a project is already done and frozen, you can run "npm run build"
  # and then it's no longer necessary to run "npm start", and also "npm install".
  [[ -s webpack-stats.json ]] && ! grep -q localhost: webpack-stats.json
}

if _in_project_path && ! _node_modules_present && ! _built_assets_present; then
  echo "$fg[green]Installing node_modules$reset_color"
  npm install
fi

unfunction _in_project_path
unfunction _node_modules_present
unfunction _built_assets_present
