# Imagen base con Python
FROM python:3.9-slim

# Instalar dependencias del sistema necesarias para PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias primero para aprovechar cache de Docker
COPY requeriments.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requeriments.txt

# Copiar el resto del código de la aplicación
COPY . .

# Puerto para Streamlit
EXPOSE 8501

# Comando de ejecución
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
