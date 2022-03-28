### Devcontainer configuration

Shared configuration is bind-mounted in the container, stored locally at ~/.local/share/magnet-django-devcontainer

To disable `Do you really want to exit ([y]/n)?` prompt of IPython, run:
```sh
ipython profile create
sed -i 's/# c.TerminalInteractiveShell.confirm_exit = True/c.TerminalInteractiveShell.confirm_exit = False/' /root/.ipython/profile_default/ipython_config.py
```
