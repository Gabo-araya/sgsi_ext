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

# Node
RUN \
  curl -fsSL https://deb.nodesource.com/setup_16.x \
    # Skip ridiculous delay
    | sed '/sleep 20/d' \
    | bash - \
  && apt-get install -y nodejs \
  # Reduce image size and prevent use of potentially obsolete lists:
  && rm -rf /var/lib/apt/lists/*

# npm and poetry
RUN \
  # Update npm:
  mkdir "$NPM_CACHE_DIR" \
  && npm install --global --cache "$NPM_CACHE_DIR" npm \
  # Delete but keeping the directory:
  && rm -rf "$NPM_CACHE_DIR"/* \
  # Ensure npm cache can be written by unprivileged users later:
  && chown $HOST_UID:$HOST_GID "$NPM_CACHE_DIR" \
  && pip install "poetry==1.4.2"


FROM dev-base as development

ARG WHO=magnet
ARG HOST_UID=2640
ARG HOST_GID=2640

# Dev utilities
RUN \
  apt-get update && apt-get install -y \
    # for Django translations:
    gettext \
    # to wait for DB:
    wait-for-it \
    # better shell:
    zsh \
    # sudo
    sudo \
    # commit inside container:
    git \
    # see container processes:
    htop \
    # parse ansible outputs:
    jq \
    # editors:
    vim nano \
    # to grep for TODOs:
    ripgrep \
    # prevents "spawn ps ENOENT" error in lint-staged:
    procps \
  && rm -rf /var/lib/apt/lists/* \
\
  # Create unprivileged user
  && groupadd --gid $HOST_GID $WHO \
  && useradd --uid $HOST_UID --gid $HOST_GID --create-home --shell /bin/zsh $WHO

RUN mkdir /usr/src/app && chown -R $HOST_UID:$HOST_GID /usr/src/app

WORKDIR /usr/src/app
COPY docker/zsh_shared docker/zsh_shared/
COPY docker/zsh_dev docker/zsh_dev/

RUN \
  # Configure oh my zsh
  sudo -u $WHO docker/zsh_dev/setup_dev.sh \
\
  # add user to sudo group
  && usermod -aG sudo --password '' $WHO \
  # Disable initial sudo lecture
  && (umask 337; echo "Defaults lecture=never" > /etc/sudoers.d/no_lecture) \
  # "install editable" ansible-ssh:
  && ln -s /usr/src/app/ansible/ansible-ssh /usr/local/bin/

# Switch to unprivileged user
USER $WHO

COPY --chown=$HOST_UID:$HOST_GID package.json package-lock.json ./
COPY --chown=$HOST_UID:$HOST_GID scripts/ ./scripts/
RUN npm ci --no-audit

# Install Poetry dev-dependencies, then ansible + collections and link `dj`.
COPY --chown=$HOST_UID:$HOST_GID pyproject.toml poetry.lock requirements.yml ./
RUN \
  poetry install -E "ansible" \
  && poetry run ansible-galaxy collection install -r requirements.yml \
  # "dj" alias available from anywhere.
  # No aliases for production, as there may not be consensus for them.
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

WORKDIR /app

COPY --from=prod-py-dependency-export /usr/src/app/requirements.txt /app/
WORKDIR /app

RUN pip install -r requirements.txt


FROM development as prod-js-builder

ARG WHO=magnet
ARG HOST_UID=2640
ARG HOST_GID=2640

ENV NODE_ENV=production

COPY --chown=$HOST_UID:$HOST_GID assets ./assets/
COPY webpack.* tsconfig.json .eslint* .stylelint* ./
RUN npm run build


FROM python:3.10-slim-bullseye AS production

ENV VIRTUAL_ENV_DISABLE_PROMPT=x

ARG WHO=magnet
ARG HOST_UID=2640
ARG HOST_GID=2640

RUN groupadd --gid $HOST_GID $WHO \
  && useradd --uid $HOST_UID --gid $HOST_GID --create-home --shell /bin/zsh $WHO

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
  # Reduce image size and prevent use of potentially obsolete lists:
  && apt-get remove -y curl gpg \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/media /app/static && chown -R $HOST_UID:$HOST_GID /app/

WORKDIR /app

COPY --from=prod-py-builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=prod-py-builder /usr/local/bin/ /usr/local/bin/
COPY --from=prod-js-builder /usr/src/app/assets/bundles/ ./assets/bundles/

COPY --chown=$HOST_UID:$HOST_GID . ./

RUN django-admin compilemessages

USER $WHO
CMD ["/usr/local/bin/prod_cmd.sh"]
