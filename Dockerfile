FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY notebook/function.py /app/
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining application code
COPY . .

# Expose Django port
EXPOSE 8000

# Command to run the application
CMD ["python", "function.py"]

# Default command to run Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]