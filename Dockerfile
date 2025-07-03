# Imagen base de Python
FROM python:3.13-alpine

# Establece directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia tus archivos al contenedor
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto (ajústalo si es un script)
CMD ["python", "main.py"]
