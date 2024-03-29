from django.contrib import admin
from .models import User, File, Classification


class UserAdmin(admin.ModelAdmin):
    list_display = ("google_drive_user_id", "user_email", "user_name", "creation_date")

class FileAdmin(admin.ModelAdmin):
    list_display = ("google_drive_file_id", "google_drive_user_id", "file_name", "file_extension", "mime_type", "classification", "visibility", "can_edit")
    ordering = ("file_extension", "file_name")  # Ordenar primero por file_extension y luego por file_name

class ClassificationAdmin(admin.ModelAdmin):
    list_display = ("poll_id", "google_drive_file_id", "classification", "creation_date", "answer_date", "commentary")
    list_filter = ("google_drive_file_id",)  # Agrega el campo para filtrar


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Classification, ClassificationAdmin)