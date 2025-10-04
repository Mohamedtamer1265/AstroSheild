# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy package files
COPY server/requirements.txt ./server/
COPY client/package*.json ./client/

# Install Python dependencies
RUN pip install --no-cache-dir -r server/requirements.txt

# Install Node.js dependencies
WORKDIR /app/client
RUN npm ci

# Copy application code
WORKDIR /app
COPY . .

# Build React frontend
WORKDIR /app/client
RUN npm run build

# Set working directory back to app
WORKDIR /app

# Expose port
EXPOSE 5000

# Set environment variable
ENV RAILWAY_ENVIRONMENT=production

# Start the application
CMD ["python", "server/run.py"]