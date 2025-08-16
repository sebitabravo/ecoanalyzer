# Imagen base de Python 3.11 slim
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    sqlite3 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Crear directorios necesarios para la aplicación
RUN mkdir -p database logs

# Establecer permisos adecuados
RUN chmod 755 database logs

# Exponer el puerto de la aplicación
EXPOSE 8081

# Variables de entorno por defecto
ENV FLASK_APP=web_app.py
ENV FLASK_ENV=production
ENV PORT=8081
ENV PYTHONUNBUFFERED=1

# Comando de inicio de la aplicación
CMD ["python", "web_app.py"]
