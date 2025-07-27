# ---------- build ----------
FROM python:3.9-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---------- runtime ----------
FROM python:3.9-slim
WORKDIR /app
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
