# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install uv
ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

# Install any needed packages specified in requirements.txt
RUN /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV PORT 8080

# Run app.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
