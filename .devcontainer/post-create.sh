# .devcontainer/post-create.sh
#!/usr/bin/env bash
set -euo pipefail

# Install Poetry
poetry config virtualenvs.in-project true --local
poetry install
poetry run pre-commit install

# 1) Bring in the Microsoft package signing key
apt-get update
apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
  gpg
curl https://packages.microsoft.com/keys/microsoft.asc \
  | gpg --dearmor \
  > /usr/share/keyrings/microsoft.gpg

# 2) Add the APT source for Functions Core Tools v4
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] \
https://packages.microsoft.com/repos/microsoft-debian-$(lsb_release -rs)-prod \
$(lsb_release -cs) main" \
  > /etc/apt/sources.list.d/azure-functions.list

# 3) Install the Core Tools
apt-get update
apt-get install -y azure-functions-core-tools-4

# (Optional) Clean up
rm -rf /var/lib/apt/lists/*