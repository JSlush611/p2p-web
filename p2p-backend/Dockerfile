# ---------- build ----------
FROM python:3.9-slim AS build
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt  

# ---------- runtime ----------
FROM python:3.9-slim
WORKDIR /app
COPY --from=build /usr/local /usr/local     
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
