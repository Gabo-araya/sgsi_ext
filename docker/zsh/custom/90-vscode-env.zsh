# When a terminal is open with vscode, some extra changes are made to that terminal.
# So if you prefer to use an independent terminal with "docker-compose exec django zsh",
# and also use git and ssh seamlessly, (https://code.visualstudio.com/docs/remote/containers#_sharing-git-credentials-with-your-container)
# open vscode in devcontainer mode, and the "postStartCommand" will write env vars to a file.
# Then when a shell is started without vscode, this script loads those vars from file.
# https://github.com/microsoft/vscode/issues/110050
#
# Also vscode copies host ~/.ssh/known_hosts to container /root/.ssh/known_hosts
# (I think it's copied only when vscode is first reopened)
# Idea: commit unhashed known_hosts to repo, and bind-mount them to /etc/ssh/ssh_known_hosts

function () {   # Scope  (https://stackoverflow.com/questions/13667284/how-do-i-keep-functions-variables-local-to-my-zshrc/13670749#13670749)
  if [[ -z "$REMOTE_CONTAINERS" ]]; then
    if [[ -r /dev/shm/env_from_vscode_terminal ]]; then

      local ignored_vars=(PATH REMOTE_CONTAINERS)

      while read line; do   # Correctly handes unquoted  https://stackoverflow.com/questions/15235729/sourcing-env-output/15248663#15248663
        local name=$(echo "$line" | sed 's/=.*//')
        if (( $ignored_vars[(Ie)$name] == 0 )); then  # "if $name not in $ignored_vars"  https://unix.stackexchange.com/questions/411304/how-do-i-check-whether-a-zsh-array-contains-a-given-value/411331#411331
          export "$line"
        fi
      done < /dev/shm/env_from_vscode_terminal

    else
      echo "$fg[yellow]vscode env not loaded$reset_color"
    fi
  fi
}
