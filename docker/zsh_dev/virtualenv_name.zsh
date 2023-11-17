function virtualenv_name {
  [[ -n "$VIRTUAL_ENV" ]] && {
    # Originally: `basename $VIRTUAL_ENV`

    # echo $VIRTUAL_ENV
    #  /home/magnet/.cache/pypoetry/virtualenvs/project-name-ASDF1234-py3.9
    venv_base="${VIRTUAL_ENV:t}"
    #  project-name-ASDF1234-py3.9
    venv_split=(${(s[-])${venv_base}})
    #  project name ASDF1234 py3.9
    venv_minus2=(${venv_split[0,-3]})
    #  project name
    venv_joined="${(j[-])venv_minus2}"
    #  project-name
    echo "$venv_joined"
  }
}
