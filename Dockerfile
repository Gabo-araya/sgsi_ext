#####################################
# Base image python + node + poetry
#####################################
FROM python:3.9.12-slim-bullseye AS project-dependencies

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ARG NPM_CACHE_DIR=/tmp/npm-cache
ARG PIP_NO_CACHE_DIR=off

# Nicer prompt is managed by zsh themes, so disable default venv prompt:
ENV VIRTUAL_ENV_DISABLE_PROMPT=x

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
\
  && title_print "Set up Node.js repository" \
  && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
\
  && title_print "Set up Postgres repository" \
  # The PostgreSQL client provides pg_isready for production, and pg_restore for development.
  && curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /usr/share/keyrings/postgresql.gpg \
  && echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
\
  && title_print "Install Postgres and Node.js" \
  && apt-get update && apt-get install -y nodejs postgresql-client-14 \
\
  && title_print "Install Poetry" \
  && pip install poetry \
\
  # Reduce image size and prevent use of potentially obsolete lists:
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev \
\
  # Remove caches to save some space
  && yes | poetry cache clear --quiet --all . \
\
  # "dj" alias available from anywhere and also in production.
  # No other aliases for production, as there may not be consensus for them.
  && ln -s /usr/src/app/manage.py "$(poetry env info --path)/bin/dj"

# Install javascript dependencies
# COPY package.json package-lock.json ./
# RUN \
#     mkdir "$NPM_CACHE_DIR" \
#     && npm ci --no-audit --cache "$NPM_CACHE_DIR" \
#     && rm -rf "$NPM_CACHE_DIR"
# TODO: delete cache

#####################################
# Production image
#####################################
# Place Production image above development, so docker-compose on servers stop building after this one.
FROM project-dependencies AS production

# Add oh-my-zsh for production
COPY docker/zsh_prod/setup_prod.sh docker/zsh_prod/setup_prod.sh
RUN docker/zsh_prod/setup_prod.sh

# COPY assets webpack.*.js ./
# RUN npm run build

# Copy rest of the project
COPY . .

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

# This was getting too long to keep in Dockerfile:
COPY docker/zsh_dev/setup_dev.sh docker/zsh_dev/setup_dev.sh

RUN \
  # Source utils containing "title_print":
  source scripts/utils.sh \
\
  && title_print "Install development utilities" \
  && apt-get update && apt-get install -y \
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
  && docker/zsh_dev/setup_dev.sh \
\
  && title_print "Finishing" \
  # Reduce image size and prevent use of potentially obsolete lists:
  && rm -rf /var/lib/apt/lists/* \
  # "install editable" ansible-ssh:
  && ln -s /usr/src/app/ansible/ansible-ssh /usr/local/bin/

# Install Poetry dev-dependencies (in separate layer because they should change more often):
RUN poetry install -E "ansible"
# FIXME: this step is super slow.

# Prevent development container shutdown:
CMD ["sleep", "inf"]

# Use bind-mounted ansible config:
ENV ANSIBLE_CONFIG=/usr/src/app/ansible/ansible.cfg
