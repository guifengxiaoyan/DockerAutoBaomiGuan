FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=Asia/Shanghai

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt flask flask-cors

COPY app.py .
COPY main.py .
COPY config.py .
COPY login.py .
COPY course.py .
COPY api_handlers.py .
COPY index.html .

EXPOSE 3000

CMD ["python3", "app.py"]
