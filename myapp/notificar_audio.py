from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from myapp.models import User, File, Classification
from pydub import AudioSegment
import speech_recognition as sr
import os
from presidio_analyzer import AnalyzerEngine
from datetime import datetime
from django.core.mail import send_mail

def download_audio_file(drive, google_drive_file_id, local_file_path):
    file = drive.CreateFile({'id': google_drive_file_id})
    file.GetContentFile(local_file_path)

def convert_audio_to_wav(input_file_path, output_file_path):
    audio = AudioSegment.from_file(input_file_path)
    audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export(output_file_path, format="wav")

def audio_to_text(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        r.adjust_for_ambient_noise(source)
        audio_data = r.record(source)
    try:
        audio_text = r.recognize_google(audio_data, language="es-AR")
        return audio_text
    except sr.UnknownValueError:
        return "No se pudo reconocer el texto"

def detect_pii_information(text):
    analyzer = AnalyzerEngine()
    results = analyzer.analyze(correlation_id="123", text=text)
    pii_entities = [e.entity_type for e in results if e.entity_type != "O"]
    return pii_entities

def notificar_audio():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # Obtener lista de archivos formato audio del inventario
    audio_files = File.objects.filter(mime_type__startswith='audio')

    for audio_file in audio_files:
        try:
            local_audio_path = audio_file.file_name
            download_audio_file(drive, audio_file.google_drive_file_id, local_audio_path)

            # Crea un archivo temporal WAV
            temp_wav_path = os.path.splitext(local_audio_path)[0] + ".wav"
            convert_audio_to_wav(local_audio_path, temp_wav_path)

            # Convierte el WAV a texto con SpeechRecognition
            audio_text = audio_to_text(temp_wav_path)
            print(f'Texto del archivo {audio_file.google_drive_file_id}: {audio_text}')

            # Elimina los archivos temporales
            os.remove(local_audio_path)
            os.remove(temp_wav_path)

            # Detecta información PII en el texto con Microsoft Presidio
            pii_entities = detect_pii_information(audio_text)
            if pii_entities:
                # Crea un nuevo registro en Classification en caso positivo
                classification = Classification.objects.create(
                    google_drive_file_id=audio_file.google_drive_file_id,
                    classification='Critico',
                    answer_date=datetime.now(),
                    commentary='Información PII detectada'
                )
                classification.save()

            """ # Envía un correo electrónico al dueño del archivo
            subject = 'Información PII detectada en archivo de audio'
            message = f"Se ha detectado información PII en el archivo de audio {audio_file.file_name}. Por favor, elimine dicho archivo de Google Drive.\n\n¡Muchas Gracias!'"
            from_email = 'your@email.com'
            recipient_list = [audio_file.google_drive_user.user_email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False) """




        except Exception as e:
            print(f"Error procesando el archivo {audio_file.google_drive_file_id}: {e}")

if __name__ == "__main__":
    notificar_audio()