#####################################
# Base image python + node + poetry
#####################################
FROM python:3.9.12-slim-bullseye AS project-dependencies

# Nicer prompt is managed by zsh themes, so disable default venv prompt:
ENV VIRTUAL_ENV_DISABLE_PROMPT=x
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

ARG NPM_CACHE_DIR=/tmp/npm-cache
ARG PIP_NO_CACHE_DIR=off

# Default users and groups
ARG WHO=magnet
ARG HOST_UID=2640
ARG HOST_GID=2640

WORKDIR /usr/src/app

# Base image already contains bash, so we can RUN with bash:
SHELL ["/bin/bash", "-c"]
# and write "source" instead of "."

# "Prints" to locate which command is running:
COPY scripts/utils.sh scripts/utils.sh
RUN \
  # Source utils containing "title_print":
  source scripts/utils.sh \
\
  && title_print "Install prerequisites" \
  && apt-get update && apt-get install -y \
    # to install from extra repositories:
    curl gnupg \
    # to compile psycopg2:
    gcc libpq-dev \
    # for Django translations:
    gettext \
    # to wait for DB:
    wait-for-it \
    # better shell:
    zsh \
    # to check for distro release and codename:
    lsb-release \
\
  && title_print "Set up Postgres repository" \
  # The PostgreSQL client provides pg_isready for production, and pg_restore for development.
  && curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /usr/share/keyrings/postgresql.gpg \
  && echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
\
  && title_print "Set up Node.js repository" \
  && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
\
  && title_print "Install Postgres and Node.js" \
  && apt-get install -y nodejs postgresql-client-14 \
  # Update npm:
  && mkdir "$NPM_CACHE_DIR" \
  && npm install --global --cache "$NPM_CACHE_DIR" npm \
  # Delete but keeping the directory:
  && rm -rf "$NPM_CACHE_DIR"/* \
  # Ensure npm cache can be written by unprivileged users later:
  && chown $HOST_UID:$HOST_GID "$NPM_CACHE_DIR" \
\
  && title_print "Install Poetry" \
  && pip install poetry \
\
  && title_print "Create non-privileged user to run apps" \
  && groupadd --gid $HOST_GID $WHO \
  && useradd --uid $HOST_UID --gid $HOST_GID --create-home --shell /bin/zsh $WHO \
\
  && title_print "Change owner of app directory" \
  && chown -R $HOST_UID:$HOST_GID . \
\
  # Reduce image size and prevent use of potentially obsolete lists:
  && rm -rf /var/lib/apt/lists/*

# Switch to unprivileged user
USER $WHO

COPY --chown=$HOST_UID:$HOST_GID pyproject.toml poetry.lock ./
RUN poetry install --no-dev \
\
  # Remove caches to save some space
  && yes | poetry cache clear --quiet --all . \
\
  # "dj" alias available from anywhere and also in production.
  # No other aliases for production, as there may not be consensus for them.
  && ln -s /usr/src/app/manage.py ~/.cache/pypoetry/virtualenvs/django3-project-template-VA82Wl8V-py3.9/bin/dj

#####################################
# Production image
#####################################
# Place Production image above development, so docker-compose on servers stop building after this one.
FROM project-dependencies AS production

ENV NODE_ENV=production
ARG NPM_CACHE_DIR=/tmp/npm-cache

ARG WHO=magnet
ARG HOST_UID=2640
ARG HOST_GID=2640

# Add oh-my-zsh for production
COPY --chown=$HOST_UID:$HOST_GID docker/zsh_prod/setup_prod.sh docker/zsh_prod/setup_prod.sh
RUN docker/zsh_prod/setup_prod.sh

# Install javascript dependencies
COPY --chown=$HOST_UID:$HOST_GID package.json package-lock.json ./
RUN \
  # Installs devDependencies, because the production image also builds the bundles:
  NODE_ENV=development npm ci --no-audit --cache "$NPM_CACHE_DIR" \
  # As /tmp is owned by root, remove only the directory contents, not the directory itself.
  && rm -rf "$NPM_CACHE_DIR"/*


# Build javascript bundles:
COPY --chown=$HOST_UID:$HOST_GID webpack.*.js ./
COPY --chown=$HOST_UID:$HOST_GID assets/ assets/
COPY --chown=$HOST_UID:$HOST_GID tsconfig.json ./
RUN npm run build

# Copy rest of the project
COPY --chown=$HOST_UID:$HOST_GID . .

RUN poetry run django-admin compilemessages

CMD ["docker/django/prod_cmd.sh"]

#####################################
# CI Test image
#####################################
FROM production AS test
# Make sure linters, style checkers and test runners get installed.
RUN poetry install

#####################################
# Development image
#####################################
FROM project-dependencies AS development
# No need to copy the whole project, it's in a volume and prevents rebuilds.

ARG WHO=magnet
ARG HOST_UID=2640
ARG HOST_GID=2640

# This was getting too long to keep in Dockerfile:
COPY --chown=$HOST_UID:$HOST_GID docker/zsh_dev/setup_dev.sh docker/zsh_dev/setup_dev.sh

# Switch to superuser as system-wide packages will need to be installed
USER root

RUN \
  # Source utils containing "title_print":
  source scripts/utils.sh \
\
  && title_print "Install development utilities" \
  && apt-get update && apt-get install -y \
    # sudo
    sudo \
    # commit inside container:
    git \
    # see container processes:
    htop \
    # parse ansible outputs:
    jq \
    # something to quickly edit a file:
    vim nano \
\
  && title_print "Install oh-my-zsh" \
  && sudo -u $WHO docker/zsh_dev/setup_dev.sh \
\
  && title_print "Finishing" \
  # add user to sudo group
  && usermod -aG sudo --password '' $WHO \
  # Disable "We trust you have received the usual lecture from...":
  && (umask 337; echo "Defaults lecture=never" > /etc/sudoers.d/no_lecture) \
  # "install editable" ansible-ssh:
  && ln -s /usr/src/app/ansible/ansible-ssh /usr/local/bin/ \
  # Reduce image size and prevent use of potentially obsolete lists:
  && rm -rf /var/lib/apt/lists/*

# Switch back to unprivileged user
USER $WHO

# Install Poetry dev-dependencies, then ansible + collections.
COPY --chown=$HOST_UID:$HOST_GID requirements.yml .
RUN \
  source scripts/utils.sh \
  && title_print "Install dev dependencies" \
  && poetry install -E "ansible" \
\
  # Install ansible collections
  && title_print "Install ansible collections" \
  && poetry run ansible-galaxy collection install -r requirements.yml

# Prevent development container shutdown:
CMD ["sleep", "inf"]

# Use bind-mounted ansible config:
ENV ANSIBLE_CONFIG=/usr/src/app/ansible/ansible.cfg
