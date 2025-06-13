FROM python:3.12.2-slim-bookworm

WORKDIR /var/www

# Copy requirements first for better caching
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y \
    procps \
    gcc \
    python3-dev \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    && apt-get remove -y gcc python3-dev \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy application code
COPY src/ src/
COPY .env .

# Create logs directory
RUN mkdir -p logs

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)" || exit 1

CMD ["python", "-m", "src.main"]