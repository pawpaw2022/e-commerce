# Use Python 3.9 slim image
FROM python:3.9-slim

# Install MySQL client
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Copy the start script
COPY start.sh .
RUN chmod +x /app/start.sh

# Expose both ports
EXPOSE 8000 8501

# Set environment variable for API URL
ENV API_URL=http://localhost:8000

# Run the start script
CMD ["/app/start.sh"]