# From dieter.zsh-theme:

# elaborate exitcode on the right when >0
return_code="%(?..%{$fg[red]%}%? ↵%{$reset_color%})"
RPS1='${return_code}'

reverse_color="\e[${color[reverse]}m"
dbname() {
  if [[ "$IS_CRITICAL_ENV" == "False" ]]; then
    local rev=
    local cased_pgdb=$PGDATABASE
  else  # Reverse and uppercase if critical env:
    local rev=$reverse_color
    # Reverse is required to get true black.  https://github.com/zsh-users/zsh/blob/41eb200d66e4bea7bc5798888a1755cdf5daa3b0/Functions/Misc/colors#L68
    local cased_pgdb=${PGDATABASE:u}
  fi

  echo -n "%{$bg[bg-black]%}%{$fg[magenta]%}%{$rev%}$cased_pgdb%{$reset_color%}"
}

# Compacted $PWD
local pwd="%{$fg[blue]%}%c%{$reset_color%}"

# From miloshadzic.zsh-theme:
local separator="%{$fg[red]%}|%{$reset_color%}"
local arrow="%{$fg[cyan]%}⇒%{$reset_color%}"

PROMPT='$(dbname) ${pwd}${separator}${arrow} '
