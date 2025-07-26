# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:0-3.12

# Install system utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      gnupg \
      lsb-release \
      unzip \
      npm && \
    rm -rf /var/lib/apt/lists/*

# Install Azure Functions Core Tools v4
RUN npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Ensure Poetry’s bin directory is on the PATH
ENV PATH="/root/.local/bin:${PATH}"
