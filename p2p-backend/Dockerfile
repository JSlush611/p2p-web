FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Set environment variables to prevent Python from writing .pyc files and to unbuffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the port Gunicorn will listen on
EXPOSE $PORT

# Command to run the application using Gunicorn
# 'app:app' assumes your Flask app instance is named 'app' in a file named 'app.py'
# Adjust the number of workers and bind address as needed
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app.app:app"]
