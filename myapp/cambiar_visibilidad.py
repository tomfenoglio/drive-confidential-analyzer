from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from .models import File, Classification
from .inventario import authenticate_with_google_drive

# Obtiene la lista de archivos que cumplen con los criterios "Critico", "Alto", can_edit=True y visibility "anyWithLink"
def get_files_to_remove_permission():
    files_to_remove_permission = []
    criticidad_list = ["Critico", "Alto"]

    for poll in Classification.objects.filter(classification__in=criticidad_list):
        file = File.objects.filter(
            google_drive_file_id=poll.google_drive_file_id,
            visibility="anyoneWithLink", # ya fue calculado en el inventario
            can_edit=True
        ).first()
        if file:
            files_to_remove_permission.append(file.google_drive_file_id)

    return files_to_remove_permission

def main():
    drive = authenticate_with_google_drive()

    files_to_remove_permission = get_files_to_remove_permission()

    # Itera sobre la lista de archivos, verifica que exista el permiso con "id": "anyoneWithLink" y lo elimina
    for file_id in files_to_remove_permission:
        file = drive.CreateFile({"id": file_id}) # Obtiene el archivo por su ID
        permissions = file.GetPermissions() # Obtiene los permisos actuales del archivo

        for permission in permissions:
            if permission["id"] == "anyoneWithLink":
                file.DeletePermission(permission["id"])
                print(f'Permiso con "id": "anyoneWithLink" eliminado con éxito para el archivo {file_id}.')
                break

if __name__ == "__main__":
    main()
