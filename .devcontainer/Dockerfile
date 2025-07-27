# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/devcontainers/python:3.12

# ─── Install Azure Functions Core Tools v4 via APT ────────────────────────────
RUN apt-get update \
    && apt-get install -y \
         apt-transport-https \
         lsb-release \
         gnupg \
         curl \
         ca-certificates \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc \
         | gpg --dearmor \
         > /usr/share/keyrings/microsoft.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] \
         https://packages.microsoft.com/repos/microsoft-debian-$(lsb_release -rs)-prod \
         $(lsb_release -cs) main" \
         > /etc/apt/sources.list.d/azure-functions.list \
    && apt-get update \
    && apt-get install -y azure-functions-core-tools-4 \
    && rm -rf /var/lib/apt/lists/*

# ─── Install Poetry ────────────────────────────────────────────────────────────
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry
