FROM python:3.12-slim

RUN useradd -ms /bin/sh -u 1001 fastapi
USER fastapi

# Change the working directory to the `app` directory
WORKDIR /app

# Copy the lockfile and `pyproject.toml` into the image
ADD --chown=fastapi:fastapi uv.lock /app/uv.lock
ADD --chown=fastapi:fastapi pyproject.toml /app/pyproject.toml

# tell uv to use system python
ENV UV_SYSTEM_PYTHON=1
ENV UV_NO_CACHE=1

# Install dependencies using uv without actually installing it
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --frozen --no-install-project --no-group dev --group production

# Copy the project into the image
COPY --chown=fastapi:fastapi . /app

COPY --chown=fastapi:fastapi ./docker/local/entrypoint /entrypoint
RUN chmod +x /entrypoint


COPY --chown=fastapi:fastapi ./docker/local/start /start
RUN chmod +x /start

USER fastapi

ENTRYPOINT ["/entrypoint"]
