FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p database logs

# Dar permisos de escritura a directorios
RUN chmod 777 database logs

# Exponer puerto
EXPOSE 8081

# Variables de entorno
ENV FLASK_APP=web_app.py
ENV FLASK_ENV=production

# Comando para ejecutar la aplicación
CMD ["python", "web_app.py"]
