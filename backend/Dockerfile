# backend/Dockerfile
FROM python:3.11-slim

# 1. Create app directory
WORKDIR /app

# 2. Install OS-level deps (if you need libpq-dev for psycopg2, etc)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your application code
COPY app ./app

# 5. Expose the port and launch Uvicorn
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
