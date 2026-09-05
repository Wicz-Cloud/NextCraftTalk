# NextCraftTalk Self-Hosted Mode Dockerfile

FROM python:3.14-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements-selfhosted.txt .

# Upgrade pip before install (CVE-2025-8869 requires >=25.3), then deps
RUN python -m pip install --upgrade "pip>=25.3" \
    && pip install --no-cache-dir -r requirements-selfhosted.txt

# Copy source code
COPY src/ ./src/

# Create data directories
RUN mkdir -p data logs

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["python", "src/main.py"]
