function virtualenv_info {
  [[ -n "$VIRTUAL_ENV" ]] && {
    # Originally: `basename $VIRTUAL_ENV`

    # echo $VIRTUAL_ENV
    #  /root/.cache/pypoetry/virtualenvs/django3-project-template-VA82Wl8V-py3.9
    venv_base="${VIRTUAL_ENV:t}"
    #  django3-project-template-VA82Wl8V-py3.9
    venv_split=(${(s[-])${venv_base}})
    #  django3 project template VA82Wl8V py3.9
    venv_minus2=(${venv_split[0,-3]})
    #  django3 project template
    venv_joined="${(j[-])venv_minus2}"
    #  django3-project-template
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
