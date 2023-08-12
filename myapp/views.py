from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from .models import Classification
from .inventario import run_inventario
from .clasificar_informacion import create_polls, calculate_classification, get_questions, get_scores
from .cambiar_visibilidad import main
from .notificar_audio import notificar_audio

def dashboard(request):
    if request.method == 'POST':
        if 'clasificar_informacion' in request.POST:
            create_polls()
            return render(request, 'dashboard.html', {'message': 'Clasificación completada'})
        elif 'cambiar_visibilidad' in request.POST:
            main()
            return render(request, 'dashboard.html', {'message': 'Restricción completada'})
        elif 'inventario' in request.POST:
            run_inventario()
            return render(request, 'dashboard.html', {'message': 'Inventario completado'})
        elif 'notificar_audio' in request.POST:
            notificar_audio()
            return render(request, 'dashboard.html', {'message': 'Notificación completada'})
    return render(request, 'dashboard.html')



def poll_view(request, poll_id):
    poll = get_object_or_404(Classification, poll_id=poll_id)
    questions = get_questions()
    scores = get_scores()

    # Deniega el acceso en caso de que el poll ya haya sido respondido
    if poll.classification != 'Pendiente':
        return redirect(reverse('access_denied'))

    # Si esta pendiente, entonces
    if request.method == 'POST':
        total_score = 0
        for question, criticity in questions.items():
            answer = request.POST.get(question, False)
            if answer:
                total_score += scores[criticity]

        classification = calculate_classification(total_score)
        poll.classification = classification
        poll.answer_date = timezone.now()
        poll.save()
        return redirect(reverse('thank_you'))

    return render(request, 'poll.html', {'poll': poll, 'questions': questions})


def access_denied_view(request):
    return render(request, 'access_denied.html')

def thank_you_view(request):
    return render(request, 'thank_you.html')
