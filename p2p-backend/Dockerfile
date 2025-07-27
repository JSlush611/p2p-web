# ---------- build ----------
FROM python:3.9-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---------- runtime ----------
FROM python:3.9-slim
WORKDIR /app
ENV PORT 8080
COPY . .
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT:-8080}", "app.app:app"]
