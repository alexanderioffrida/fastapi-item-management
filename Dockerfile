# ============================================
# Stage 1: Builder
# ============================================
# Pinned digest for reproducible builds (python:3.12-alpine as of 2026-01-16)
FROM python:3.12-alpine@sha256:68d81cd281ee785f48cdadecb6130d05ec6957f1249814570dc90e5100d3b146 AS builder

WORKDIR /app

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.12-alpine@sha256:68d81cd281ee785f48cdadecb6130d05ec6957f1249814570dc90e5100d3b146 AS runtime

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY main.py models.py ./

EXPOSE 8000

RUN adduser --disabled-password --home /home/appuser appuser
USER appuser

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]