from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from myapp.models import User, File, Classification
from django.db.models import Q

def get_or_create_user(gdrive_user):
    user, created = User.objects.get_or_create(
        google_drive_user_id=gdrive_user["id"],
        defaults={
            "user_email": gdrive_user["emailAddress"],
            "user_name": gdrive_user["displayName"]
        }
    )
    return user

def get_visibility(permissions):
    for permission in permissions:
        if permission["id"] == "anyoneWithLink":
            return "anyoneWithLink"
    return "Restricted"

# Trae el valor de la ultima clasificación ejecutada
def get_classification(google_drive_file_id):
    try:
        classification = Classification.objects.filter(Q(google_drive_file_id=google_drive_file_id) & ~Q(classification="Anulado")).latest("answer_date")
        return classification.classification
    except Classification.DoesNotExist:
        return ""

def run_inventario():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # Obtiene lista de archivos (propios y compartidos) en Google Drive, excluye las carpetas y archivos en papelera
    file_list = drive.ListFile({"q": "trashed=false and mimeType != 'application/vnd.google-apps.folder'"}).GetList()

    # Borra todos los registros de la tabla File
    File.objects.all().delete()

    # Procesa la lista de archivos y la guarda en la base de datos
    for file in file_list:
        user, created = User.objects.get_or_create(
            google_drive_user_id=file["owners"][0]["permissionId"],
            defaults={"user_email": file["owners"][0]["emailAddress"], "user_name": file["owners"][0]["displayName"]}
        )

        # Obtiene la visibilidad
        file_obj = drive.CreateFile({"id": file["id"]})
        permissions = file_obj.GetPermissions()
        visibility = get_visibility(permissions)

       # Obtiene la extensión del archivo, si no existe, asigna el MIME Type de Google
        mime_type = file["mimeType"]
        file_extension = file.get("fileExtension")
        if not file_extension:
            mime_type_parts = mime_type.split(".")
            if len(mime_type_parts) > 1:
                file_extension = mime_type_parts[-1]
            else:
                file_extension = "sin extensión"

        classification = get_classification(file["id"])
        File.objects.create(
            google_drive_file_id=file["id"],
            google_drive_user_id=user,
            file_name=file["title"],
            file_extension=file_extension,
            can_edit=file["capabilities"]["canEdit"],
            visibility=visibility,
            mime_type=mime_type,
            classification=classification
        )

if __name__ == "__main__":
    run_inventario()