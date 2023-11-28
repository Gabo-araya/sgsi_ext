# Django Project Template™

Django Project Template™ provides a common starting point for Django projects, it provides known and tested approaches for the most common features found on Magnet projects.
This is the recommended way for starting a new project.

## Getting started

### Get the code

Create a new repository for your django project and clone your repository into
your computer.

Add the magnet-dpt bitbucket repo as a remote repository:

* `git remote add template git@bitbucket.org:magnet-cl/magnet-dpt.git`

Pull the code from the project template:

* `git pull template main`

Search and replace all occurrences of `project-name-placeholder` to your desired project name

Configure `git_repo` in `ansible/group_vars/all.yaml`

Push to your own repo:

* `git push origin master`

Now you have your own django project in your repository.

Remove the `LICENSE` if your new project does not have an MIT license.

### Quickstart

The `quickstart.sh` script includes the following actions:

* Create a local .env file if not present.
* Install docker and compose plugin.
* Build and start the containers.
* Prompt to run django migrations.
* Prompt to create a superuser.
* Apply settings to use vscode devcontainers.

### Running the project

1. Reboot your computer if quickstart prompted to do so (to run Docker without sudo)
2. Open this folder in VSCode
3. Click "Reopen in Container" when prompted (or press F1 and choose "Reopen in Container")

<details>
<summary>CLI alternative</summary>

1. Open VSCode and make sure the `Dev Containers` extension is enabled.
2. In the Command Palette (F1), run `Dev Containers: Install devcontainer CLI`.
3. When asked to create a symlink to the `devcontainer` tool, click the "Create" button.

Code will install the `devcontainer` tool on your PATH, meaning meaning you can now run

```sh
devcontainer open
```

to open the project.
</details>

Then in a VSCode terminal, run:

```sh
npm start
```

and in another terminal, run:

```sh
djs
```

and access the site at http://localhost:8000

#### "Without" VSCode

Note: commands written here with [oh-my-zsh aliases](https://github.com/ohmyzsh/ohmyzsh/blob/master/plugins/docker-compose/docker-compose.plugin.zsh).

In a terminal in this folder,

- Start the containers with `dcupd` (faster), or rebuilding with `dcupb -d` (slower but may be required)
- Spawn a container shell with `dce django zsh`
- If it printed _vscode env not loaded_, then you are missing [some features provided by VSCode](https://code.visualstudio.com/docs/remote/containers#_sharing-git-credentials-with-your-container) and may have problems using Git. To fix this:
  - Outside the container, run `devcontainer open` (see "CLI alternative" above)
  - Wait for VSCode and the container to load, and hide its window somewhere.
  - Now you may use `dce django zsh` to run django and node and git. And an alternative IDE to edit files. Unfortunately you have to keep the VSCode window open.
  - For how this works, see `90-vscode-env.zsh` in this repo.

#### Resetting to initial state

If you are used to work with docker-compose, you may try to reset your project to an initial state with `docker compose down -v`. However we are not using volumes, just bind mounts. So use instead:

```sh
docker compose down
rm -rf docker/volumes/
git restore docker/volumes/
```

### Start a new django application

Use the custom app template to create your apps:

`python manage.py startapp {app_name} --model-name [model_name]`

The app template assumes your app name is a plural, the `model_name` parameter is optional. The template contains the following:

- A model that is named the same as your app, but in singular. The model name
  can be changed by passing the `model_name` parameter to the `startapp`
  command.
- A `views.py` file with all CRUD views for the model.
- A `urls.py` file mapping all CRUD views.
- A `managers.py` file with a single QuerySet for the model
- A `forms.py` file with a single Form for the model
- An `admin.py` file with a single Admin for the model
- A `templates` folder with templates in HTML format for all CRUD views.

### Changes to .env file while developing

If you change your .env file, you'll need to rebuild your container for the setting to take effect. You can do this by running the `Remote-Containers: Rebuild Container` command in the Command Palette (`F1`) when you are connected to the container.

This takes time, you can press the `(show log)` button to view the progress.

## Changes from the previous version

### Django 4.2 LTS

This template is based on Django 4.2.x, which is supported up to mid-2026. Some introduced features are:

* psycopg 3 support
* Comments on columns and tables
* Constraint validation
* Migrations are automatically formatted using Black if present
* In-memory file storage, useful for tests
* Custom file storages
* Native Redis caching
* Template-based form rendering
* Updated admin site with system font stack and dark/light theme support
* Hardened password hashing
* Support for prefetching sliced QuerySets
* Asynchronous support for ORM and view handlers.

Some deprecations are, but not limit to:
* `pytz` in favor of standard `zoneinfo`
* Database support for:
  * MariaDB <= 10.3
  * MySQL <= 5.7
  * PostgreSQL <= 11
* Support for `MemcachedCache` backend
* `index_together` option in favor of `indexes`
* Passing encoded JSON string literals to JSONField
* `BaseUserManager.make_random_password()`. Use `secrets` instead
* `DEFAULT_FILE_STORAGE` and `STATICFILES_STORAGE`. Use `STORAGES["default"]` and `STORAGES["staticfiles"]` instead
* Log out via GET, use POST instead
* DeleteView now uses FormMixin to handle POST requests. Any custom deletion logic in delete() handlers should be moved to form_valid(), or a shared helper method, if required.

Future changes are:
* Setting update_fields in Model.save() may now be required

### TypeScript and Vite

[TODO]

### React

React is installed in this template and can be used to implement custom components.

#### Component autoloader

An autoloader is provided, that creates a new React root and mounts components in the container you want. To register a component to be mounted in a container, register it in `assets/ts/index.ts`:

```typescript
import { YourReactComponent } from ...;
...
ComponentLoader.registerComponent('#selectorId .or-class-name', YourReactComponent);
```

#### Props for auto-loaded components

If the container you defined includes a data attribute `data-props-source-id="some-id"`, a json with that id will be searched in the body, parsed as json, and passed as props to your component. These jsons are generated in the templates with a `{{props_data|json_script:'some-id'}}` tag.

You can view an example in `assets/ts/components/example-component` for react, and `base/templates/index.html` for the backend side.

#### Django context for React

Additionally, components are mounted inside a DjangoContext.Provider, which provides global values from the backend. These values can be accessed from any react component that is mounted with the autoloader, like this:

```typescript jsx
import {DjangoContext} from '../../contexts/django-context';
...
const djangoContext = useContext(DjangoContext);
return <p>{djangoContext?.user.id}</p>
```

In this example, the current user id of the logged user in Django is shown in React.

The contents of this global context can be extended in the `react_context` context processor in `base/context_processors.py`

### Documentation
Previous information found on this file can be now found in the `docs/` directory.

## Troubleshooting

### Very strange errors occur when running `git commit`

Because there's a hook which uses pre-commit, lint-staged and other tools, if they are not properly installed then the commit will be prevented.

Examples of these errors are:

_Command not found: pre-commit_<br>
_SyntaxError: The requested module 'supports-color' does not provide an export named 'default'_

and they all end with:

```
husky - pre-commit hook exited with code 1 (error)
```

To fix this:

1. Ensure that if you have local changes to:

- package.json
- package-lock.json
- pyproject.toml
- poetry.lock

then they are reasonable. (For example the version of lint-staged hasn't been changed by mistake)

2. Reinstall npm packages with `npm ci` and Poetry packages with `poetry install`

##### `zsh: command not found: dj`

If for some reason the virtualenv is deleted, `poetry install` won't recreate the `dj` symlink, it has to be manually created again with:

```sh
ln -s /usr/src/app/manage.py $(poetry env info --path)/bin/dj
```

Or just recreate the container (as the symlink is included in the image).
