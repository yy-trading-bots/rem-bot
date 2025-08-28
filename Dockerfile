FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

VOLUME ["/app/data"]

CMD ["python", "main.py"]