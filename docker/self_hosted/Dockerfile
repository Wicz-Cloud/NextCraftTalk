# NextCraftTalk Self-Hosted Mode Dockerfile

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (optional - can be run separately)
# RUN curl -fsSL https://ollama.ai/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements-selfhosted.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-selfhosted.txt

# Copy source code
COPY src/ ./src/
COPY main.py .

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
CMD ["python", "main.py"]
