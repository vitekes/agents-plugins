FROM python:3.12-slim

WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash --uid 1000 plugin && \
    chown -R plugin:plugin /app

USER plugin

# Copy only necessary files
COPY --chown=plugin:plugin manifest.json .
COPY --chown=plugin:plugin src/ ./src/
COPY --chown=plugin:plugin requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for HTTP interface
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Run the plugin
CMD ["python", "-u", "src/main.py"]
