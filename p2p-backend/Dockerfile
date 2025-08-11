FROM python:3.9-slim-buster

WORKDIR /app

# Prevent .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

EXPOSE ${PORT}

CMD exec gunicorn --bind :${PORT} --workers 1 --threads 8 --timeout 0 run:app