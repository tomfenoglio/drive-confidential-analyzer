from myapp.models import File, Classification
from django.core.mail import send_mail
from django.urls import reverse
import json
import os

def get_questions():
    questions_path = os.path.join(os.path.dirname(__file__), "questions.json")
    with open(questions_path, "r") as archivo:
        questions = json.load(archivo)

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