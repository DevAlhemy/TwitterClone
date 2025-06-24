FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env.template .env

EXPOSE 8000

CMD ["sh", "-c", \
    "cd app && \
     ./backup/restore.sh && \
     uvicorn main:app --host 0.0.0.0 --port 8000"]
