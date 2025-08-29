# 1. Build stage
FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
# This creates a .venv in /app
RUN uv sync --no-dev

# Copy the rest of the application code
COPY . .


# 2. Final stage
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment and the application code from the build stage
COPY --from=builder /app /app

# Make port 8080 available
EXPOSE 8080
ENV PORT=8080

# Activate the virtual environment and run the application
ENV PATH="/app/.venv/bin:${PATH}"
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "winedentity:app"]
