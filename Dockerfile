# syntax=docker/dockerfile:1.7

###############################################################################
# agentforge-shared - base image & development stage
###############################################################################
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN groupadd --gid 1000 app && useradd --gid 1000 --uid 1000 --create-home app

COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

###############################################################################
# Builder: install project with system dependencies
###############################################################################
FROM base AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md CHANGELOG.md LICENSE ./
COPY src ./src

RUN python -m pip install --upgrade pip build

###############################################################################
# Production image: lean, installs only runtime wheels
###############################################################################
FROM base AS runtime

COPY --from=builder /app /app

RUN python -m pip install --no-deps /app \
    && rm -rf /app

USER app

# Healthcheck: validates the package imports correctly.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import agentforge_shared, sys; sys.exit(0)"

CMD ["python", "-c", "import agentforge_shared; print(agentforge_shared.__version__)"]

###############################################################################
# Test stage: full dev toolchain, runs the entire suite
###############################################################################
FROM base AS test

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md CHANGELOG.md LICENSE ./
COPY src ./src
COPY tests ./tests
COPY examples ./examples

RUN python -m pip install --upgrade pip \
    && python -m pip install pytest pytest-asyncio pytest-cov ruff mypy bandit orjson
RUN python -m pip install --no-deps .

CMD ["pytest", "--cov=agentforge_shared", "--cov-report=term-missing"]