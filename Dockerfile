# 1. Build stage
FROM python:3.13-slim as builder

# Create a virtual environment
RUN python -m venv /opt/venv

# Copy requirements file
COPY requirements.txt .

# Install uv and then immediately use it to install dependencies in a single layer.
# This avoids any PATH issues. Finally, clean up.
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    /root/.cargo/bin/uv pip install --no-cache -r requirements.txt -p /opt/venv/bin/python && \
    apt-get remove -y curl && \
    apt-get clean

# 2. Final stage
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the build stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code
COPY . .

# Make port 8080 available
EXPOSE 8080
ENV PORT 8080

# Activate the virtual environment and run the application
ENV PATH="/opt/venv/bin:${PATH}"
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
