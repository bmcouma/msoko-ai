# ─── Msoko AI — Dockerfile ────────────────────────────────────────────────────
# Multi-stage build for minimal production image (Python 3.12 slim)
# Optimized for Railway / Render / any Docker host

# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Prevent .pyc files and enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install OS-level build dependencies (for psycopg2-binary etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into /install for copying
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# ── Stage 2: Runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Runtime OS libs (libpq for psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy the entire project
COPY . .

# Collect static files during build
RUN python backend/manage.py collectstatic --noinput --settings=msoko_backend.settings

# Copy and prepare entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create a non-root user for security
RUN addgroup --system msoko && adduser --system --ingroup msoko msoko
RUN chown -R msoko:msoko /app
USER msoko

EXPOSE $PORT

ENTRYPOINT ["/app/entrypoint.sh"]
# Gunicorn entry point — loads app from backend/
CMD ["sh", "-c", "gunicorn msoko_backend.wsgi:application --chdir backend --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 --log-level info"]
