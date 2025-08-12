FROM python:3.11-slim-bullseye

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV ASM3_ROOT=/app

# Create app directory
WORKDIR $ASM3_ROOT

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Core dependencies
    make \
    curl \
    # Python dependencies for ASM3
    python3-dev \
    python3-pip \
    # Image processing
    python3-pil \
    imagemagick \
    # PDF generation
    wkhtmltopdf \
    # PostgreSQL development headers (needed for psycopg2-binary)
    libpq-dev \
    # Development tools (optional, can be removed for production)
    nodejs \
    npm \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages that might not be available as system packages
RUN pip3 install --no-cache-dir \
    cheroot \
    python-memcached \
    psycopg2-binary \
    requests \
    boto3 \
    reportlab \
    xhtml2pdf \
    lxml \
    openpyxl \
    qrcode \
    stripe

# Copy the application code
COPY . $ASM3_ROOT/

# Generate version file and build assets
RUN cd $ASM3_ROOT && \
    npm install && \
    make version && \
    make rollup && \
    rm -rf node_modules

# Create necessary directories
RUN mkdir -p /var/log \
    && mkdir -p /tmp/asm_disk_cache \
    && chmod 755 /tmp/asm_disk_cache

# Create a startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Wait for database to be ready\n\
echo "Waiting for database..."\n\
while ! nc -z postgres 5432; do\n\
  sleep 1\n\
done\n\
echo "Database is ready!"\n\
\n\
# Start ASM3\n\
echo "Starting ASM3..."\n\
cd /app/src\n\
exec python3 main.py 5000\n\
' > /app/start.sh && chmod +x /app/start.sh

# Install netcat for database health check
RUN apt-get update && apt-get install -y netcat && apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose the port
EXPOSE 5000

# Set the working directory to src for running
WORKDIR $ASM3_ROOT/src

# Use the startup script
CMD ["/app/start.sh"]