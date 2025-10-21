# Use Python 3.11 alpine for minimal size
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Install minimal system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    curl \
    && rm -rf /var/cache/apk/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

# Copy only necessary application files
COPY app.py .
COPY api_openrouter.py .
COPY apps_script_service.py .
COPY google_sheets_service.py .
COPY hybrid_sheets_service.py .
COPY simple_sheets_service.py .
COPY public_sheets_solution.py .
COPY templates/ ./templates/

# Create logs directory
RUN mkdir -p logs

# Create non-root user
RUN adduser -D -s /bin/sh app && \
    chown -R app:app /app
USER app

# Expose port
EXPOSE 8081

# Simple health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=2 \
    CMD curl -f http://localhost:8081/api/data || exit 1

# Run the application
CMD ["python", "app.py"]
