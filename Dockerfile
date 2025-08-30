FROM python:3.11.6-alpine3.18

ENV PIP_DISABLE_PIP_VERSION_CHECK 1 \
    PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    UV_CACHE_DIR=/root/.cache/uv

WORKDIR /app

RUN apk add --no-cache \
    curl ca-certificates

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

COPY . .
