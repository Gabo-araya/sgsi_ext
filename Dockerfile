#####################################
# Base image python + node + poetry
#####################################
FROM python:3.9.9-slim-bullseye AS python-node-base

WORKDIR /usr/src/app

# Base image already contains bash, so we can RUN with bash:
SHELL ["/bin/bash", "-c"]
# and write "source" instead of "."

# Install prerequisites
RUN apt-get update && apt-get install -y gcc curl libpq-dev gettext \
  && rm -rf /var/lib/apt/lists/*

# Install Node
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
  && apt-get install -y nodejs \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

#####################################
# Add python+node dependencies
#####################################
FROM python-node-base AS project-dependencies
# Install python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Install javascript dependencies
# COPY package.json package-lock.json ./
# RUN npm ci

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
# TODO: zsh with poetry shell, dj aliases and scary production theme ($PGDATABASE as prompt)

CMD ["docker/django/production_cmd.sh"]

#####################################
# Development image
#####################################
FROM project-dependencies AS development

# No need to copy the whole project, it's in a volume and prevents rebuilds.

# "Prints" to locate which command is running:
COPY scripts/utils.sh scripts/utils.sh

RUN \
  # Source utils containing "title_print":
  source scripts/utils.sh \
\
  # PostgreSQL client is required to pg_restore from Django container into Postgres container.
\
  && title_print "Adding Postgres repo" \
  && curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /usr/share/keyrings/postgresql.gpg \
  && echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
\
  && title_print "apt update + install" \
  && apt-get update && apt-get install -y \
    # better shell:
    zsh \
    # commit inside container:
    git \
    # see container processes:
    htop \
    # parse ansible outputs:
    jq \
    # postgres-client programs:
    postgresql-client-14 \
    # something to quickly edit a file:
    vim nano \
\
  && title_print "Installing oh-my-zsh" \
  # base installation:
  && sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
  # customization:
  && ln -s /usr/src/app/docker/load-devcontainer-customs.zsh /root/.oh-my-zsh/custom/ \
  && ln -s /usr/src/app/docker/zshcustom/ /root/.oh-my-zsh/custom/project \
  # /root/.oh-my-zsh/custom/shared will be bind-mounted by compose
\
  && title_print "Finishing" \
  # Reduce image size and prevent use of potentially obsolete lists:
  && rm -rf /var/lib/apt/lists/* \
  # "install editable" ansible-ssh:
  && ln -s /usr/src/app/ansible/ansible-ssh /usr/local/bin/

# Install Poetry dev-dependencies (in separate layer because they should change less often):
RUN poetry install

# Prevent development container shutdown:
CMD ["sleep", "inf"]

# Use bind-mounted ansible config:
ENV ANSIBLE_CONFIG=/usr/src/app/ansible/ansible.cfg
