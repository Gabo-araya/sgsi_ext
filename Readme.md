### Devcontainer configuration

#### Shared configuration

Shared configuration is bind-mounted in the container, stored locally at ~/.local/share/magnet-django-devcontainer

TODO: how to add and override aliases

#### Disable IPython exit prompt

To disable `Do you really want to exit ([y]/n)?` prompt of IPython, run:
```sh
ipython profile create
sed -i 's/# c.TerminalInteractiveShell.confirm_exit = True/c.TerminalInteractiveShell.confirm_exit = False/' /root/.ipython/profile_default/ipython_config.py
```

### Solving `poetry.lock` merge conflicts

If `pyproject.toml` is not conflicted, and the only conflict in `poetry.lock` is:
```toml
content-hash = "..."
```
you can solve it by running this inside the devcontainer:
```sh
git restore --staged --worktree poetry.lock && poetry lock --no-update && git add poetry.lock
```


### User Authentication
#### Inactive users
The built-in forms and views support displaying a message when their accounts
exist but were deactivated. However, the respective code paths won't execute
when using the default `ModelBackend` for authentication and they will be
considered as they never existed. This is a deliberate design decision by part
of Django developers.

If you really need to display such a message, consider using a different backend
for authentication such as `AllowAllUsersModelBackend`.
