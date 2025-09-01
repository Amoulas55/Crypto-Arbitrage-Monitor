# Lightweight Python image
FROM python:3.12-slim

# Working directory inside container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run script
CMD ["python", "arbitrage_monitor.py"]
