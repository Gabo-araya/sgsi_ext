#####################################
# Base image python + node + poetry
#####################################
FROM python:3.9.9-slim-bullseye AS python-node-base

WORKDIR /usr/src/app

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
# COPY django/package.json django/package-lock.json ./
# RUN npm install

#####################################
# Development image
#####################################
FROM project-dependencies AS development
# No need to copy the project, it's in a volume and prevents rebuilds.
# Install Poetry dev-dependencies:
RUN poetry install
RUN apt-get update && apt-get install -y git htop zsh \
  && sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
  && rm -rf /var/lib/apt/lists/*
# Prevent development container shutdown
CMD ["/bin/sh", "-c", "\"while sleep 1000; do :; done\""]

#####################################
# Production image
#####################################
FROM project-dependencies AS production
# Copy rest of the project
COPY . .
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
