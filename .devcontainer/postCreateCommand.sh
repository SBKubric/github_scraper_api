#! /usr/bin/env bash

export WORKSPACES_NAME="api"
echo "Setting up git..."
if [ -d "/workspaces/${WORKSPACES_NAME}/.git" ]; then
    git rm -rf /workspaces/${WORKSPACES_NAME}/.git
    git init
    git remote add origin git@github.com:SBKubric/github_scraper_api.git
fi

git fetch origin
git checkout --force main

echo "git set up"

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Install Dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install --install-hooks


if [-d "/workspaces/${WORKSPACES_NAME}/.env/local"]; then
    echo "Setting up .env/local..."
    for env_file in "/workspaces/${WORKSPACES_NAME}/.env/local"; do
        if [ -f "$env_file" ]; then
            export $(grep -v '^#' "$env_file" | xargs)
        fi
    done
    echo "Set up .env/local!"
fi
