# 1. Build stage
FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

WORKDIR /app

COPY . /app

RUN uv sync --locked --no-install-project --no-dev

RUN uv sync --locked --no-dev

# 2. Final stage
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the build stage
COPY --from=builder --chown=app:app /app /app

# Copy the application code
COPY . .

# Make port 8080 available
EXPOSE 8080
ENV PORT=8080

# Activate the virtual environment and run the application
ENV PATH="/app/.venv/bin:${PATH}"
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
