### Devcontainer configuration

#### Shared configuration

The configuration files in your computer stored in `~/.local/share/magnet-django-devcontainer` are shared to all django devcontainers. This stores zsh and ipython histories, and other customizations.

In this folder, in `zshcustom/50-aliases.zsh` you may customize your aliases. This file is only created once (by quickstart.sh if it doesn't exist), and never automatically modified later.

You can add other `zshcustom/*.zsh` files, which are loaded when zsh starts. You can also add and commit `docker/zsh_dev/custom/*.zsh` files so they apply to all developers.

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

### Javascript debugging

In development, webpack is configured to produce simple sourcemaps, because nice sourcemaps take too long to generate in large projects.

The downside is that for example when debugging in the browser the `render()` of a React component, it looks like this:

![ugly code](.readme_images/js_cheap-eval-source-map.png)

You can change, in `webpack.dev.js`, the `devtool` option so it looks like this:

![original code](.readme_images/js_eval-source-map.png)
