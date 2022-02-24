# Load custom configurations inside "project" and "shared" folders:
for config_file ("$ZSH_CUSTOM"/{project,shared}/*.zsh(N)); do
  source "$config_file"
done
# It's better to have the configurations grouped in folders, which are then symlinked and bind-mounted.
# As oh-my-zsh doesn't load files from subfolders of $ZSH_CUSTOM, this file does.
