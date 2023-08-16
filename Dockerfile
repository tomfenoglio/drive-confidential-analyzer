# Usa una imagen de Python como base
FROM python:3.8

# Ahora hay que definir paso por paso como seria toda la instalación del proyecto
# Establece variables de entorno para no escribir en la terminal interactiva durante la instalación
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Crea una carpeta en el contenedor y se ubica dentro de ella para la ejecución de los proximos comandos
WORKDIR /app

# Copia todo el contenido de la carpeta donde esta este archivo a la imagen del contenedor que estamos creando. Si queremos ignorar ciertos archivos en la imagen del contenedor, hay que crear un ".dockerignore" (como git)
COPY . /app/

# Instala FFmpeg en el environment (necesario para usar la libreria PyDub)
RUN apt-get update && \
    apt-get install -y ffmpeg

# Instala las dependencias del proyecto (numpy tuve que sacar la version en requirements.txt porque daba error)
RUN pip install -r requirements.txt

# Indicar qué puertos se desean utilizar para la comunicación con el exterior del contenedor. Tener en cuenta que esto solo documenta la intención de exponer esos puertos, y aún necesitarás configurar el mapeo de puertos al ejecutar el contenedor (a traves de docker-compose.yml).
EXPOSE 8000
EXPOSE 8080

# Cuando se inicie el contenedor que se cree a partir de la imagen de este Dockerfile, se va a ejecutar:
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]