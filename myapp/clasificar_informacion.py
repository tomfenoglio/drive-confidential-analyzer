from myapp.models import File, Classification
from django.core.mail import send_mail
from django.urls import reverse

def get_questions():
    questions = {
    "Información que permita/ayude a descubrir la identidad de una persona (información personal identificable - PII). Ejemplo: nombres, dni, direcciones, email, teléfono, patente vehiculo, fecha nacimiento, etc.": "Critico",
    "Información financiera confidencial, como estados de cuenta, datos bancarios o informes de inversiones?": "Critico",
    "Información médica. Ejemplo: datos médicos, historiales de salud, diagnósticos, registros médicos y cualquier otra información relacionada con la salud de los individuos.": "Critico",
    "Contraseñas y/o credenciales. Ejemplo: claves de acceso, credenciales de inicio de sesión y cualquier otra información que permita el acceso no autorizado a sistemas o cuentas.": "Critico",
    "Propiedad intelectual y secretos comerciales. Ejemplos: Planes de negocio, diseños de productos, estrategias de marketing, patentes, información de investigación y desarrollo, y otros secretos comerciales.": "Critico",
    "Su pérdida o divulgación podría causar interrupciones significativas en los procesos comerciales.": "Critico",
    "La divulgación no autorizada de este archivo podría resultar en multas o sanciones regulatorias.": "Critico",
    "Datos de clientes, proveedores o socios comerciales.": "Alto",
    "Comunicaciones sensibles: Correos electrónicos, mensajes de chat o cualquier comunicación que contenga información confidencial o estratégica.": "Alto",
    "Contratos, acuerdos o documentos legales de la empresa.": "Alto",
    "Información relacionada con la estrategia de seguridad de la empresa.": "Alto",
    "Contiene información que solo debería ser accesible para un grupo selecto de personas.": "Alto",
    "Es un archivo esencial para la operación diaria de la empresa.": "Alto",
    "Información regulada por leyes.": "Alto",
    "Documentación legal. Ejemplos: Contratos, acuerdos legales, documentación de litigios y cualquier otra información relacionada con asuntos legales.": "Alto",
    "Materiales de Marketing Genéricos: Folletos, presentaciones y materiales de marketing de productos o servicios que no contengan detalles estratégicos o confidenciales.": "Medio",
    "Políticas y Procedimientos Estándar: Documentos que describen las políticas y procedimientos estándar de la empresa que no contienen información estratégica o detallada.": "Medio",
    "Información de la Compañía para Clientes: Materiales destinados a clientes que proporcionan información general sobre la empresa y sus servicios.": "Medio",
    "Presentaciones de Información Pública: Presentaciones utilizadas en conferencias o charlas públicas que no incluyen información estratégica sensible.": "Medio",
    "Materiales de Entrenamiento Interno: Recursos de entrenamiento y desarrollo profesional para empleados que no contienen datos altamente confidenciales o estratégicos.": "Medio"
    }
    return questions

def get_scores():
    scores = {
        "Critico":10000,
        "Alto":1000,
        "Medio":10
    }
    return scores

def calculate_classification(total_score):
    score_grade = get_scores()
    if total_score >= score_grade["Critico"]:
        return 'Critico'
    elif total_score >= score_grade["Alto"]:
        return "Alto"
    elif total_score >= score_grade["Medio"]:
        return "Medio"
    else:
        return 'Bajo'


def create_polls():
    files = File.objects.all()

    for file in files:
        classification = 'Pendiente'
        poll = Classification.objects.create(
            google_drive_file_id=file.google_drive_file_id,
            classification=classification
        )

        # Construye el link del cuestionario
        poll_id = poll.poll_id
        poll_link = reverse('poll_url', kwargs={'poll_id': poll_id})

        # Obtiene el nombre y la extension del archivo
        file_name = file.file_name

        # Envia el email con el link a su dueño
        subject = 'Cuestionario para clasificar archivo'
        message = f'Por favor, complete el cuestionario para clasificar su archivo "{file_name}". Haga click en el siguiente link:\n\nhttp://127.0.0.1:8000{poll_link}\n\n¡Muchas Gracias!'
        from_email = 'your@email.com'
        recipient_list = [file.google_drive_user.user_email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

if __name__ == "__main__":
    create_polls()