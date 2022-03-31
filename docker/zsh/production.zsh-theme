# From dieter.zsh-theme:

# local time, color coded by last return code
time_enabled="%(?.%{$fg[green]%}.%{$fg[red]%})%*%{$reset_color%}"
time_disabled="%{$fg[green]%}%*%{$reset_color%}"
time=$time_enabled

# elaborate exitcode on the right when >0
return_code_enabled="%(?..%{$fg[red]%}%? ↵%{$reset_color%})"
return_code_disabled=
return_code=$return_code_enabled

RPS1='${return_code}'

# Clear errors with enter:
function accept-line-or-clear-warning () {
	if [[ -z $BUFFER ]]; then
		time=$time_disabled
		return_code=$return_code_disabled
	else
		time=$time_enabled
		return_code=$return_code_enabled
	fi
	zle accept-line
}
zle -N accept-line-or-clear-warning
bindkey '^M' accept-line-or-clear-warning

reverse_color="\e[${color[reverse]}m"
dbname() {
  # Reverse if name contains "prod":
  case "$PGDATABASE" in
    *prod*)
      local rev=$reverse_color
    ;;
  esac
  # Reverse is required to get true black.  https://github.com/zsh-users/zsh/blob/41eb200d66e4bea7bc5798888a1755cdf5daa3b0/Functions/Misc/colors#L68

  echo -n "%{$bg[bg-black]%}%{$fg[yellow]%}%{$rev%}$PGDATABASE%{$reset_color%}"
}

# Compacted $PWD
local pwd="%{$fg[blue]%}%c%{$reset_color%}"

# From miloshadzic.zsh-theme:
local separator="%{$fg[red]%}|%{$reset_color%}"
local arrow="%{$fg[cyan]%}⇒%{$reset_color%}"

PROMPT='${time} $(dbname) ${pwd}${separator}${arrow} '
