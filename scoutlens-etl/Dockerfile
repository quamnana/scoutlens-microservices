FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install qdrant-client

RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/
COPY dataset/ ./dataset/

CMD ["python", "scripts/etl_script.py"]
