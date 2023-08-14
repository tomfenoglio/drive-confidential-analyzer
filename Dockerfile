# Usa una imagen de Python como base
FROM python:3.8

# Establece variables de entorno para no escribir en la terminal interactiva durante la instalación
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Esto lo agregué porque FFmpeg es necesario para usar PyDub y desde requirements daba error
RUN apt-get update && \
    apt-get install -y ffmpeg

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Copia el contenido de tu proyecto al directorio de trabajo del contenedor
COPY . /app/

# Expone el puerto en el que se ejecutará el servidor de Django
EXPOSE 8000

# Comando para ejecutar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


