# PDC App Framework — Dockerfile estándar
# ⚠️ NO MODIFICAR. Generado y mantenido por IT — Integraciones Digitales.
# El pipeline CI/CD construye esta imagen automáticamente en PDC Deploy.

FROM python:3.11-slim

WORKDIR /srv/app

# Forzar HTTPS en los repos de Debian — evita bloqueos de red/proxy sobre HTTP plano
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources

# Dependencias del sistema necesarias para psycopg2 / oracledb
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app/main.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--browser.gatherUsageStats=false"]
