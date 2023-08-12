from django.db import models
import uuid

class User(models.Model):
    google_drive_user_id = models.CharField(primary_key=True, max_length=255)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.google_drive_user_id}'

class File(models.Model):
    google_drive_file_id = models.CharField(primary_key=True, max_length=255)
    google_drive_user = models.ForeignKey('User', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_extension = models.CharField(max_length=20)
    mime_type = models.CharField(max_length=200)
    visibility = models.CharField(max_length=20)
    can_edit = models.BooleanField()
    classification = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.google_drive_file_id}'

class Classification(models.Model):
    poll_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    google_drive_file_id = models.CharField(max_length=255)
    CLASSIFICATION_CHOICES = (
        ('Critico', 'Critico'),
        ('Alto', 'Alto'),
        ('Medio', 'Medio'),
        ('Bajo', 'Bajo'),
        ('Pendiente', 'Pendiente'),
        ('Anulado', 'Anulado'),
    )
    classification = models.CharField(max_length=10, choices=CLASSIFICATION_CHOICES, default='Pendiente')
    creation_date = models.DateTimeField(auto_now_add=True)
    answer_date = models.DateTimeField(null=True, blank=True)
    commentary = models.CharField(max_length=200)


    def __str__(self):
        return f'{self.poll_id}'