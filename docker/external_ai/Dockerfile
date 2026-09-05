# NextCraftTalk External AI Mode Dockerfile

FROM python:3.14-alpine

# Set working directory
WORKDIR /app

# Install system dependencies and build tools
# Avoid brittle exact apk version pins that break as Alpine indexes move.
RUN apk add --no-cache \
    curl \
    build-base \
    gcc \
    g++ \
    && rm -rf /var/cache/apk/*

# Copy requirements first for better caching
COPY requirements-external.txt .

# Upgrade pip before install (CVE-2025-8869 requires >=25.3), then deps
RUN python -m pip install --upgrade "pip>=25.3" \
    && pip install --no-cache-dir -r requirements-external.txt

# Remove build dependencies and create non-root user
RUN apk del build-base gcc g++ \
    && adduser -D -h /home/app -s /bin/sh app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
ENV PYTHONPATH=/app
CMD ["python", "src/main.py"]
