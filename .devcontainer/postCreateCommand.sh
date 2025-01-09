#! /usr/bin/env bash

git rm -rf .git
git init
git remote add origin git@github.com:SBKubric/github_scraper_api.git
git fetch origin
git checkout --force main

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install --install-hooks
