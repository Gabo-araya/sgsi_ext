function virtualenv_info {
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
    echo %F{blue}"($venv_joined) "%f
  }
}

PROMPT='$(virtualenv_info)'
PROMPT+="%(?:%{$fg_bold[green]%}➜ :%{$fg_bold[red]%}➜ )"
PROMPT+=' %{$fg[cyan]%}%c%{$reset_color%} $(git_prompt_info)'

ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg_bold[blue]%}git:(%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%} "
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[blue]%}) %{$fg[yellow]%}✗"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[blue]%})"
