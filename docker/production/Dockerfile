# Install uv
FROM python:3.12-slim

# Change the working directory to the `app` directory
WORKDIR /app

# Copy the lockfile and `pyproject.toml` into the image
ADD uv.lock /app/uv.lock
ADD pyproject.toml /app/pyproject.toml

# tell uv to use system python
ENV UV_SYSTEM_PYTHON=1

# Install dependencies using uv without actually installing it
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --frozen --no-install-project --no-group dev --group production

# Copy the project into the image
ADD . /app

ENTRYPOINT ["/entrypoint"]
