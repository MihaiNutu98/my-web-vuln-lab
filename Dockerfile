# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app folder
COPY app/ ./app

# Expose port
EXPOSE 5000

# Run the app from the subfolder
CMD ["python", "app/app.py"]
