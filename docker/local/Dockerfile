# Install uv
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd -ms /bin/sh -u 1001 fastapi

# Change the working directory to the `app` directory
WORKDIR /app

# Copy the lockfile and `pyproject.toml` into the image
ADD uv.lock /app/uv.lock
ADD pyproject.toml /app/pyproject.toml

RUN uv sync

# Copy the project into the image
COPY --chown=fastapi:fastapi . /app

COPY --chown=fastapi:fastapi ./docker/production/entrypoint /entrypoint
RUN chmod +x /entrypoint


COPY --chown=fastapi:fastapi ./docker/local/start /start
RUN chmod +x /start

USER fastapi
ENTRYPOINT ["/entrypoint"]
