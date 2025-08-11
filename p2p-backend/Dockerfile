FROM python:3.9-slim-buster

WORKDIR /app

# Prevent .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Default command if not overridden by docker-compose
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:5000"]