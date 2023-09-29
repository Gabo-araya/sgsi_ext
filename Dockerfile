# Base image with Postgres 15 libraries
FROM python:3.10-bullseye AS dev-base-pg15

# Base image already contains bash, so we can RUN with bash
# and write "source" instead of "."
SHELL ["/bin/bash", "-c"]

# Base dependencies
RUN \
  apt-get update && apt-get install -y \
    # to compile python native bindings:
    gcc \
    # to check for distro release and codename:
    lsb-release \
  # Reduce image size and prevent use of potentially obsolete lists:
  && rm -rf /var/lib/apt/lists/*

# Postgres
RUN \
  # The PostgreSQL client provides pg_isready for production, and pg_restore for development.
  curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /usr/share/keyrings/postgresql.gpg \
  && echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
  && apt-get update && apt-get install -y libpq-dev postgresql-client-15 \
  # Reduce image size and prevent use of potentially obsolete lists:
  && rm -rf /var/lib/apt/lists/*


FROM dev-base-pg15 AS dev-base

# Nicer prompt is managed by zsh themes, so disable default venv prompt:
ENV VIRTUAL_ENV_DISABLE_PROMPT=x
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

# Custom but reliable way to know if running inside container, and easily fakeable:
ENV RUNNING_IN_CONTAINER=x

ARG NPM_CACHE_DIR=/tmp/npm-cache
ARG PIP_NO_CACHE_DIR=off

ARG WHO=magnet
ARG HOST_UID=2640
ARG HOST_GID=2640
ARG NODE_MAJOR=18

# Dev tools
RUN \
  apt-get update && apt-get install -y \
    # for Django translations:
    gettext \
    # commit inside container:
    git \
    # actually non-slim version already includes git, but sadly not all it's recommended packages
    # (specifically "less"), so include them explicitly:
    ca-certificates patch less ssh-client \
    # required for node setup
    curl gnupg  \
    # parse ansible outputs:
    jq \
  && rm -rf /var/lib/apt/lists/*

# Node
RUN \
  mkdir -p /etc/apt/keyrings \
  && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
    | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
  && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" \
    | tee /etc/apt/sources.list.d/nodesource.list \
  && apt-get update && apt-get install -y nodejs \
  # Update npm:
  && mkdir "$NPM_CACHE_DIR" \
  && npm install --global --cache "$NPM_CACHE_DIR" npm \
  # Delete but keeping the directory:
  && rm -rf "$NPM_CACHE_DIR"/* \
  # Ensure npm cache can be written by unprivileged users later:
  && chown $HOST_UID:$HOST_GID "$NPM_CACHE_DIR" \
  # Reduce image size and prevent use of potentially obsolete lists:
  && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip install "poetry==1.4.2"

# Create unprivileged user
RUN \
  groupadd --gid $HOST_GID $WHO \
  && useradd --uid $HOST_UID --gid $HOST_GID --create-home $WHO

RUN mkdir /usr/src/app && chown -R $HOST_UID:$HOST_GID /usr/src/app

# Switch to unprivileged user
USER $WHO

WORKDIR /usr/src/app

COPY --chown=$HOST_UID:$HOST_GID scripts/ ./scripts/

# Install Poetry dev-dependencies
COPY --chown=$HOST_UID:$HOST_GID pyproject.toml poetry.lock ./
RUN poetry install --with dev


FROM dev-base as development

ARG WHO=magnet
ARG HOST_UID=2640
ARG HOST_GID=2640

USER root

# Dev utilities
RUN \
  apt-get update && apt-get install -y \
    # to wait for DB:
    wait-for-it \
    # better shell:
    zsh \
    # sudo
    sudo \
    # see container processes:
    htop \
    # editors:
    vim nano \
    # to grep for TODOs:
    ripgrep \
    # prevents "spawn ps ENOENT" error in lint-staged:
    procps \
  && rm -rf /var/lib/apt/lists/*

COPY docker/zsh_shared docker/zsh_shared/
COPY docker/zsh_dev docker/zsh_dev/

RUN \
  # Configure oh my zsh
  sudo -u $WHO docker/zsh_dev/setup_dev.sh \
  # "install editable" ansible-ssh:
  && ln -s /usr/src/app/ansible/ansible-ssh /usr/local/bin/ \
  # add user to sudo group, set zsh as default shell
  && usermod -aG sudo --password '' -s /bin/zsh $WHO \
  # Disable initial sudo lecture
  && (umask 337; echo "Defaults lecture=never" > /etc/sudoers.d/no_lecture)

# Switch back to unprivileged user
USER $WHO

# Install ansible + collections and link `dj`.
COPY --chown=$HOST_UID:$HOST_GID requirements.yml ./
RUN \
  poetry install --with=deploy-tools \
  && poetry run ansible-galaxy collection install -r requirements.yml \
  # "dj" alias available from anywhere.
  && ln -s /usr/src/app/manage.py $(poetry env info --path)/bin/dj

# Prevent development container shutdown:
CMD ["sleep", "inf"]

# Use bind-mounted ansible config:
ENV ANSIBLE_CONFIG=/usr/src/app/ansible/ansible.cfg


# This stage is used to generate a static requirements.txt file for production builds
FROM dev-base as prod-py-dependency-export

WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes -o requirements.txt


FROM dev-base-pg15 AS prod-py-builder

WORKDIR /usr/src/app

ARG PIP_NO_CACHE_DIR=off
COPY --from=prod-py-dependency-export /usr/src/app/requirements.txt /usr/src/app/
RUN pip install -r requirements.txt


FROM dev-base as prod-js-builder

ARG WHO=magnet
ARG HOST_UID=2640
ARG HOST_GID=2640

ENV NODE_ENV=production

COPY --chown=$HOST_UID:$HOST_GID package.json package-lock.json ./
# Empty "--omit" because devDependencies are currently required to build:
RUN npm ci --omit="" --no-audit \
  && rm -rf "$NPM_CACHE_DIR"/*

COPY --chown=$HOST_UID:$HOST_GID assets ./assets/
COPY vite.config.ts tsconfig.json .eslint* .stylelint* ./
RUN npm run build


FROM dev-base as test

COPY . ./
COPY --from=prod-js-builder /usr/src/app/assets/bundles/ ./assets/bundles/


FROM python:3.10-slim-bullseye AS production

ARG WHO=magnet
ARG HOST_UID=2640
ARG HOST_GID=2640

RUN groupadd --gid $HOST_GID $WHO \
  && useradd --uid $HOST_UID --gid $HOST_GID --create-home --shell /bin/zsh $WHO

WORKDIR /usr/src/app

COPY docker/zsh_shared docker/zsh_shared/
COPY docker/zsh_prod docker/zsh_prod/

# System dependencies
RUN \
  apt-get update && apt-get install -y --no-install-recommends \
    gettext \
    libssl1.1 \
    libxml2 \
    lsb-release \
    shared-mime-info \
    wait-for-it \
    zsh \
    curl \
    gpg \
  # The PostgreSQL client provides pg_isready for production, and pg_restore for development.
  && curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /usr/share/keyrings/postgresql.gpg \
  && echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
  && apt-get update && apt-get install -y libpq5 postgresql-client-15 \
  # oh-my-zsh: (requires curl. "su" instead of multiple layers with RUN-USER-RUN-USER-RUN)
  && su $WHO docker/zsh_prod/setup_prod.sh \
  # Reduce image size and prevent use of potentially obsolete lists:
  && apt-get remove -y curl gpg \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app/media /usr/src/app/static && chown -R $HOST_UID:$HOST_GID /usr/src/app/

COPY --from=prod-py-builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=prod-py-builder /usr/local/bin/ /usr/local/bin/
COPY --from=prod-js-builder /usr/src/app/assets/bundles/ ./assets/bundles/

COPY --chown=$HOST_UID:$HOST_GID . ./
COPY --chown=$HOST_UID:$HOST_GID ./docker/django/prod_cmd.sh ./

RUN ln -s /usr/src/app/manage.py /usr/local/bin/dj

USER $WHO
RUN django-admin compilemessages

# Set git version and build time before finishing to reduce build time
# when only minor changes are done
ARG GIT_REF="<unknown>"
ENV GIT_REF=$GIT_REF
ARG BUILD_TIME="<unknown>"
ENV BUILD_TIME=$BUILD_TIME

CMD ["/usr/src/app/prod_cmd.sh"]
