# Use Python 3.14
FROM python:3.14-slim

# Prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

# Prevent .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Working directory
WORKDIR /app

# Install Linux packages
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch

RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]