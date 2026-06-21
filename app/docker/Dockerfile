FROM python:3.12-slim

# 1. Kunci install paket sistem di paling atas (Biarlah ini jalan lama SEKALI SAJA)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Amankan pip cache dengan COPY requirements terpisah
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# 3. File kode ditaruh paling bawah agar kalau ada edit kode, layer atas GAK AKAN diulang
COPY app/ .

EXPOSE 5000

CMD ["gunicorn", "-c", "docker/gunicorn_config.py", "run:app"]
