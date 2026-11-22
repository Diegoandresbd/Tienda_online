# 1. Usa una imagen oficial y ligera de Python como base
FROM python:3.11-slim

# 2. Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copia el archivo de dependencias e instálalas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia el resto de tu código de la aplicación
COPY . .

# 5. Expone el puerto 5000 (el puerto por donde saldrá nuestra web)
EXPOSE 5000

# 6. Comando para ejecutar la aplicación Flask cuando el contenedor inicie
CMD ["flask", "run", "--host=0.0.0.0"]