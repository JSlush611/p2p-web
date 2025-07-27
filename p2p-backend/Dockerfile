FROM python:3.9-slim-buster

WORKDIR /app

# Prevent .pyc files, unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080            

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080                   

# Use shell form so $PORT is expanded at runtime
CMD gunicorn --bind "0.0.0.0:${PORT}" app.app:app
