FROM python:3.12-slim

WORKDIR /app

# Dependências do sistema (necessário para mysqlclient / cryptography etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# O comando real fica no docker-compose (migrate + seed + run)
CMD ["flask", "--app", "wsgi", "run", "--host=0.0.0.0", "--port=5000"]