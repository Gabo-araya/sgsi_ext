##~  NOTE: this is the file commited in repository.
##~  Changes here won't apply to your terminal.
##~  Instead you may want to edit this one: (outside of container)
##~    ~/.config/magnet-django-devcontainer/zshcustom/50-aliases.zsh

alias djs='dj runserver_plus'
alias djs0='djs 0:8000'
alias djs9='djs 0:9000'
alias djsh='dj shell_plus'
alias djshp='dj shell_plus --print-sql'
alias djdbsh='dj dbshell'
alias djr='./reset.sh'
alias djcc='dj clear_cache'
alias djm='dj migrate'
alias djmm='dj makemigrations'

djt() {
  if [[ "$1" == "--help" ]]; then
    echo 'usage: djt [-cefn]
  -c is --create-db
  -e is --exitfirst
  -f is --failed-first
  -n is --new-first

Runs "pytest --reuse-db" adding extra arguments with shortcuts.'
    return 0
  fi

  local c= e= f= n=
  while getopts cefn opt; do
    case $opt in
      c) c=--create-db ;;  # Correctly overrides --reuse-db, as documented in "pytest --help"
      e) e=--exitfirst ;;
      f) f=--failed-first ;;
      n) n=--new-first ;;
      ?) return 1
    esac
  done

  pytest --reuse-db $c $e $f $n "$@"
}


# Note: "dj" is not an alias, but a symlink created in Dockerfile.
