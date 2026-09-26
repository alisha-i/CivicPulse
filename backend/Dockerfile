# Stage 1: Build environment
FROM python:3.11-slim as build-env

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime environment
FROM python:3.11-slim as runtime

# Create a non-root user
RUN useradd -m -s /bin/bash appuser
USER appuser

WORKDIR /app

# Copy dependencies from build-env
COPY --from=build-env /root/.local /home/appuser/.local

# Ensure local bin is in PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application code (excluding tests and scripts via .dockerignore, or explicitly)
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser alembic.ini ./
COPY --chown=appuser:appuser alembic/ ./alembic/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
