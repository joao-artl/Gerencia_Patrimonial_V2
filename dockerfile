FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd curl && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .