# Use official Python image
FROM python:3.11-slim

WORKDIR /app

# Copy requirements & install
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "run.py"]
