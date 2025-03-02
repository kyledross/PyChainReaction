# Use Python 3.12 base image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies required for pygame and X11, including PipeWire
RUN apt-get update && apt-get install -y \
  libsdl2-2.0-0 \
  libsdl2-mixer-2.0-0 \
  libsdl2-image-2.0-0 \
  pipewire \
  pipewire-audio-client-libraries \
  libspa-0.2-modules \
  wireplumber \
  libx11-6 \
  x11-utils \
  xauth \
  libxext6 \
  && rm -rf /var/lib/apt/lists/*

# Create a non-root user with your host UID
RUN useradd -u 1000 -m gameuser && \
  chown -R gameuser:gameuser /app

# Set environment variable for XDG_RUNTIME_DIR
ENV XDG_RUNTIME_DIR=/run/user/1000

# Create and set correct permissions for runtime directory
RUN mkdir -p /run/user/1000 && \
  chown -R gameuser:gameuser /run/user/1000 && \
  chmod 700 /run/user/1000

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .
RUN chown -R gameuser:gameuser /app

# Switch to the non-root user
USER gameuser

# Command to run your application directly
CMD ["python", "src/main.py"]