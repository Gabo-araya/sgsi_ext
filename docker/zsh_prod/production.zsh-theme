# From dieter.zsh-theme:

# elaborate exitcode on the right when >0
return_code="%(?..%{$fg[red]%}%? ↵%{$reset_color%})"
RPS1='${return_code}'

if [[ "$ENVIRONMENT_NAME" == "production" ]]; then
  local envname="PRODUCTION"
  local reverse_color="\e[${color[reverse]}m"
  local rev=$reverse_color
  # Reverse is required to get true black.  https://github.com/zsh-users/zsh/blob/41eb200d66e4bea7bc5798888a1755cdf5daa3b0/Functions/Misc/colors#L68
else
  local envname="$ENVIRONMENT_NAME"
  local rev=
fi

local proj_env_name="$(echo -n "%{$bg[bg-black]%}%{$fg[magenta]%}%{$rev%}$PROJECT_NAME-$envname%{$reset_color%}")"

# Compacted $PWD
local pwd="%{$fg[blue]%}%c%{$reset_color%}"

# From miloshadzic.zsh-theme:
local separator="%{$fg[red]%}|%{$reset_color%}"
local arrow="%{$fg[cyan]%}⇒%{$reset_color%}"

PROMPT='${proj_env_name} ${pwd}${separator}${arrow} '
