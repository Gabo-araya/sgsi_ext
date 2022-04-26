# aptinst: runs "apt update" if absolutely necessary, and then "apt install ..."

function aptinst {
  # "if /var/lib/apt/lists is empty" https://stackoverflow.com/questions/91368/checking-from-shell-script-if-a-directory-contains-files/50751686#50751686
  for _ in /var/lib/apt/lists(N/^F); do
    sudo apt update
  done

  sudo apt install -y "$@"
}
