#####################################
# Base image python + node + poetry
#####################################
FROM python:3.9.9-slim-bullseye AS python-node-base

WORKDIR /usr/src/app

# Install prerequisites
RUN apt-get update && apt-get install -y gcc curl libpq-dev gettext

# Install Node
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

# Clean apt lists
RUN rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

#####################################
# Add python+node dependencies
#####################################
FROM python-node-base AS development
# Install python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install

# Install javascript dependencies
# COPY django/package.json django/package-lock.json ./
# RUN npm install

# Copy rest of the project
COPY . .

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
