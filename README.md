# Drive Confidential Analyzer 🛡️
## Descripción
Es una app desarrollada en Django (Python) para analizar archivos de una unidad de Google Drive con el objetivo de evitar la fuga de información confidencial. Permite realizar las siguientes operaciones:
- Guardar en una base de datos MySQL información sobre todos los archivos contenidos en la unidad de Google Drive.
- Clasificar dichos archivos en alguna de las categorías (Crítico, Alto, Medio y Bajo) a través del envío automático de un cuestionario al dueño de los mismos. El cuestionario se envia a través de un link que contiene un checklist de preguntas que según sus respuestas,se define una criticidad que se modifica automáticamente en la base de datos.
- Modificar la visibilidad de los archivos compartidos con alta criticidad a `Privado`.
- Visualizar historial de cambios de criticidad en los archivos.
- Analizar archivos de audio para detectar contenido con información de identificación personal (PII) y en caso positivo, clasificar dichos archivos como `Crítico` y notificar al dueño vía email con una sugerencia de que debe borrarlos de Google Drive por contener información de alta confidencialidad.

## Instrucciones de instalación
Sigue estos pasos para ejecutar la aplicación:

1. Clona este repositorio desde GitHub a tu máquina local.
2. Navega a la ubicación del proyecto en la terminal y ejecuta `pipenv install` para instalar las dependencias.
3. Configura la base de datos en `settings.py` con la información de MySQL.
4. Configura el servidor de email en `settings.py` para el envío automático de cuestionarios y notificaciones por email. En el caso de Gmail, primero hay que ir a la configuración de Gmail, activar la verificación en dos pasos y luego generar una contraseña para aplicaciones.
5. Configura las credenciales para la API de Google Drive. Sigue las instrucciones en la documentación de PyDrive para obtener las credenciales de OAuth2 y colocar el archivo client_secrets.json en la raíz de tu proyecto.
6. Instalar el modelo NLP de Spacy en español corriendo `python -m spacy download es_core_news_md` para que Microsoft Presidio pueda detectar info PII en español. Acá están todos los lenguajes: https://spacy.io/models/es.
instalar ffmep en el sistema para que pueda funcionar PyDub, no en python.
7. Activa el entorno virtual con `pipenv shell` y ejecuta las migraciones con `python3 manage.py migrate`.
8. Inicia el servidor con `python3 manage.py runserver`.

## Instrucciones de uso
La app tiene las siguientes 4 funciones que se pueden acceder a traves [Dashboard](http://127.0.0.1:8000/dashboard):
- **Inventariar archivos**: Crea una base de datos en MySQL de todos los archivos encontrados en la unidad de Google Drive.El campo "Classification" trae la última Criticidad definida (si existe).
- **Clasificar información de todos los archivos**: Envia por email al dueño de cada archivo, un link con acceso a un cuestionario para definir la Criticidad de forma automática a partir de las respuestas. Todos los cambios de clasificación se registran en la tabla "Classification" de la base de datos.
- **Restringir archivos públicos de alta criticidad**: Cambia la visibilidad a "Privado" en la configuración de Google Drive de todos los archivos que cumplen los siguientes criterios: Clasificación "Critico", "Alto", can_edit=True y visibility "anyWithLink".
- **Notificar audios con información PII**: Busca los archivos de audio en Google Drive, los convierte a formato WAV para luego poder ser convertidos a texto con SpeechRecognition, busca información PII con Microsoft Presidio y en caso de detección positiva, envía un email al dueño del archivo sugiriendo su eliminación y le asigna "Critico" como clasificación en la base datos (además agrega el comentario "Información PII detectada" para diferenciar dicha clasificación respecto a las de origen de cuestionario).

Para acceder a las visualizaciones de la base de datos:
- [Admin](http://127.0.0.1:8000/admin) (Superusuario: admin, Contraseña: admin@123!)


## Dependencias utilizadas
- **Django**: Dicho framework aporta significativos beneficios como seguridad integrada, un robusto sistema de autenticación y autorización que permite controlar roles y permisos de usuarios y otras soluciones de seguridad avanzadas.
- **PyDrive**: El uso de PyDrive proporciona una capa de abstracción sobre la API de Google Drive, simplificando el proceso de autenticación y manejo de archivos y carpetas.
- **MySQLclient**: Es un conector de Python para la base de datos MySQL. Permite que una aplicación escrita en Python se comunique y trabaje con una base de datos MySQL.
- **PyDub**: Libreria que nos permite realizar conversión de formato de ficheros de audio. Se debe tener instalado ffmep.
- **SpeechRecognition**: Es una biblioteca de Python que sirve para procesar y transcribir el habla humana en texto.
- **Spacy**: Spacy proporciona modelos NLP (Natural Language Processing) que permiten a Presidio reconocer entidades y realizar otras tareas lingüísticas clave para su funcionamiento. Ademas de la instalacion de Presidio, se debe instalar el modelo NLP en español por separado.
- **Microsoft Presidio**: Es una plataforma de código abierto desarrollada por Microsoft que se utiliza para el análisis y protección de datos sensibles en entornos empresariales. Su principal objetivo es ayudar a las organizaciones a identificar, clasificar y proteger información confidencial y personal en grandes volúmenes de datos, como texto.

## Supuestos
- Se considera que visibilidad `privada` se refiere al estado `restringido` del acceso general dentro de las opciones de compartir y que visibilidad `pública`, se refiere al estado `Cualquier persona que tenga el vínculo`.
- De acuerdo a la consigna, la app no analiza carpetas, solo todos los archivos que se encuentren en el Google Drive del usuario en cuestión. Es decir, si un archivo está configurado como `privado` pero lo contiene una carpeta configurada como `pública`, cualquier persona que disponga del link de esa carpeta compartida, puede acceder a dicho archivo. Por ende, con esta metodología, no deberían compartirse carpetas a fin de evitar dicho riesgo.
- Solo se podrá modificar la visibilidad de aquellos archivos a los cuales se tengan permisos de edición en Google Drive. Para lograr esto, se debe borrar a través del método `permissions.delete` de la API de Google Drive, los permisos que tengan `id`: `anyoneWithLink`.
- La app permite responder el cuestionario de un archivo por una única vez. Para volver a cambiar la clasificación, se debe generar un nuevo `poll_id`, es decir, volver a correr el script `clasificar_informacion.py` y generar un nuevo cuestionario. De esta manera queda un registro de todos los cambios que hubo en la clasificación a través de la app.
- La visualización de la base de datos, se realiza directamente en el administrador de Django con user `admin` y contraseña `admin@123!`. En este caso, el usuario admin tiene activado todos los permisos pero se pueden crear todos los usuarios que se deseen, con permisos y roles específicos de una manera muy sencilla. Para visualizar la evolución del cambio de la clasificación de los archivos, hay que simplemente hacer click en la tabla `Poll`.

## Problemas y Soluciones
- No todos los archivos en Google Drive tienen extensión. Por ejemplo, archivos de Google Docs, Google Drawings, Google Forms, Google Jamboard, Google My Maps, Google Slides, Google Sheets, etc. En esos casos, me pareció apropiado obtener el valor del MIME Type. Por ejemplo: si el archivo no tiene extensión y su MIME Type es `application/vnd.google-apps.document` (es decir un Google Doc) entonces se debe asignar el valor de `document` como extensión.

## Criterios para clasificar la información
Los criterios a tener en cuenta para el diseño de las preguntas de clasificación de confidencialidad de los archivos son: sensibilidad de la información, propiedad intelectual y secretos comerciales, impacto operativo, cumplimiento normativo, documentación legal, niveles de acceso y si hay algun riesgo de que la divulgación de dicha información impacte negativamente de alguna forma en la empresa y/o individuos internos y externos.
La clasificación de criticidad puede ser alguna de las siguientes:
- **Critico**: Información que no debe ser almacenada en este tipo de repositorio. Por ejemplo, información PII, información financiera confidencial, información médica de individuos, contraseñas y/o credenciales, propiedad intelectual y secretos comerciales confidenciales, información confidencial sensible a multas o sanciones regulatorias.
- **Alto**: Información que puede ser almacenada en este tipo de repositorio pero solo de forma privada. Es decir, solo a personas a las cuales implícitamente se les compartió el archivo de forma particular. Por ejemplo: datos de clientes, proveedores o socios comerciales (que no estén incluidos como PII), documentación legal como contratos, acuerdos legales, documentación de litigios y cualquier otra información relacionada con asuntos legales, datos anónimos de usuarios: Información estadística o datos agregados de usuarios/clientes que no revelan información personal identificable, políticas y procedimientos estándar: documentos de políticas y procedimientos que son relevantes para toda la empresa y no contienen información crítica, materiales de entrenamiento interno: recursos de entrenamiento y desarrollo profesional para empleados que no contienen datos altamente confidenciales o estratégicos.
- **Medio**:  Información que puede ser almacenada en este tipo de repositorio e inclusive de forma pública. Por ejemplo: materiales de eventos públicos: anuncios y promociones de eventos públicos o conferencias en las que la empresa participe, documentos de investigación no confidenciales: resultados de investigaciones o estudios que no contienen información sensible o secreta, información de eventos sociales de la empresa: detalles de eventos internos, como celebraciones de aniversario, actividades de equipo y eventos sociales, información de la compañía para clientes: materiales destinados a clientes que proporcionan información general sobre la empresa y sus servicios, materiales de investigación general: resultados generales de investigaciones o estudios que no incluyen detalles confidenciales, comunicados Internos no sensibles: anuncios y comunicados internos sobre eventos, cambios organizativos o logros que no contienen información confidencial.
- **Bajo**: Toda información de baja confidencialidad que no pertenece a alguna de las clasificaciones anteriores y puede almacenarse en este repositorio y de forma pública sin ningún tipo de riesgo. Algunos ejemplos: información de contacto pública: detalles de contacto generales de la empresa, como números de teléfono y direcciones de correo electrónico publicar, contenido educativo público: cursos en línea, seminarios web y otros materiales educativos que la empresa ofrezca al público en general.

Utilicé un sistema de puntos para definir la clasificación con las respuestas del cuestionario. Cada clasificación de criticidad debe ser mayor o igual a un puntaje total: Crítica -> 10.000 puntos, Alta -> 1.000 puntos, Media -> 10 Puntos.
Todas las preguntas son de respuesta boolean y en caso verdadero, suman la cantidad de puntos de la criticidad que representan. Por ejemplo: una pregunta que si es respondida como `True` es `Critica`, entonces suma 100.000 puntos. Si su criticidad es `Media`, entonces suma `10` puntos. De esta forma es muy sencillo poder hacer modificaciones en las preguntas sin necesidad de modificar la lógica del programa.