#####################################
# Base image python + node + poetry
#####################################
FROM python:3.9.12-slim-bullseye AS project-dependencies

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ARG NPM_CACHE_DIR=/tmp/npm-cache
ARG PIP_NO_CACHE_DIR=off


WORKDIR /usr/src/app

# Base image already contains bash, so we can RUN with bash:
SHELL ["/bin/bash", "-c"]
# and write "source" instead of "."

# NOTE: use "Prints" to easily see which command is running:
COPY scripts/utils.sh scripts/utils.sh
RUN \
  # Source utils containing "title_print":
  source scripts/utils.sh \
\
  && title_print "Install prerequisites" \
  && apt-get update && apt-get install -y gcc curl gnupg libpq-dev gettext wait-for-it \
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
  # Install python dependencies
  source scripts/utils.sh \
  && title_print "Install Poetry" \
  && pip install poetry \
\
  # Reduce image size and prevent use of potentially obsolete lists:
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN \
    poetry install --no-dev \
\
    # Remove caches to save some space
    && yes | poetry cache clear --quiet --all .

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

# COPY assets webpack.*.js ./
# RUN npm run build

# Copy rest of the project
COPY . .

RUN poetry run django-admin compilemessages

# TODO: django-cron
# TODO: source poetry env in entrypoint
# TODO: zsh with dj aliases and scary production theme ($PGDATABASE as prompt)
# TODO: ipython history in a volume

CMD ["docker/django/production_cmd.sh"]

#####################################
# Development image
#####################################
FROM project-dependencies AS development

# No need to copy the whole project, it's in a volume and prevents rebuilds.

# This was getting too long to keep in Dockerfile:
COPY docker/zsh/setup.sh docker/zsh/setup.sh

RUN \
  # Source utils containing "title_print":
  source scripts/utils.sh \
\
  && title_print "Install development utilities" \
  && apt-get update && apt-get install -y \
    # better shell:
    zsh \
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
  && docker/zsh/setup.sh \
\
  && title_print "Finishing" \
  # Reduce image size and prevent use of potentially obsolete lists:
  && rm -rf /var/lib/apt/lists/* \
  # "install editable" ansible-ssh:
  && ln -s /usr/src/app/ansible/ansible-ssh /usr/local/bin/

# Install Poetry dev-dependencies (in separate layer because they should change more often):
RUN poetry install
# FIXME: this step is super slow.

# Prevent development container shutdown:
CMD ["sleep", "inf"]

# Use bind-mounted ansible config:
ENV ANSIBLE_CONFIG=/usr/src/app/ansible/ansible.cfg
