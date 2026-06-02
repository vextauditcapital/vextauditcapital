# ================================================================================
# VEXT AUDIT CAPITAL — ENTERPRISE DOCKER BUILD SPECIFICATION
# ================================================================================
# Use official python slim image for lightweight containerisation and minimal vulnerability surface
FROM python:3.11-slim as builder

# Set build-time variables and prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /install

# Install system dependencies required for compiling C/C++ based libraries (like psycopg2, reportlab)
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependency file first to leverage Docker's build cache layers
COPY requirements.txt /requirements.txt

# Install python dependencies into a isolated directory
RUN pip install --no-cache-dir --prefix=/install -r /requirements.txt

# --- STAGE 2: FINAL ULTRA-LIGHTWEIGHT RUNTIME IMAGE ---
FROM python:3.11-slim as runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    APP_ENV=production

WORKDIR /app

# Install standard runtime dependencies (libpq required for PostgreSQL connectivity)
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq5 \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /app/logs /app/invoices /app/reports

# Copy pre-compiled dependencies from stage 1
COPY --from=builder /install /usr/local

# Copy application and agent assets into container space
COPY app/ /app/app/
COPY agents/ /app/agents/
COPY sitemap.xml /app/sitemap.xml
COPY robots.txt /app/robots.txt

# Create a secure, non-privileged system user to run execution processes
# satisfy SOC 2 & ISO 27001 compliance rules (never run process as root)
RUN groupadd -r vextuser && useradd -r -g vextuser vextuser && \
    chown -R vextuser:vextuser /app

USER vextuser

# Google Cloud Run binds natively to $PORT environment variable
EXPOSE 8080

# Command to execute the FastAPI Gateway production web server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
