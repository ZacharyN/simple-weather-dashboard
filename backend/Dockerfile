FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

# Port configuration (can be overridden via environment variable)
ARG BACKEND_PORT=8000
ENV BACKEND_PORT=${BACKEND_PORT}
EXPOSE ${BACKEND_PORT}

# Run application
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${BACKEND_PORT}"]
