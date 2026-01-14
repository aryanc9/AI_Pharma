FROM python:3.9-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (cache optimization)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY backend backend
COPY pharmacy.db pharmacy.db

# Environment
ENV APP_ENV=prod
ENV DB_PATH=/app/pharmacy.db
ENV LLM_PROVIDER=ollama
ENV OLLAMA_MODEL=llama3.1:8b

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
