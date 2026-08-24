FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN groupadd --gid 1000 app \
 && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash app

ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    UV_CACHE_DIR=/app/.uv-cache \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app
