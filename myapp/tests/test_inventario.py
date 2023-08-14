import unittest
from unittest.mock import patch, MagicMock
from myapp.models import User, File, Classification
from myapp.inventario import authenticate_with_google_drive, get_or_create_user, get_visibility, get_classification, inventario

class TestInventario(unittest.TestCase):
    @patch('myapp.inventario.GoogleAuth')
    @patch('myapp.inventario.GoogleDrive')
    def test_authenticate_with_google_drive(self, mock_GoogleDrive, mock_GoogleAuth):
        # Configurar objetos simulados para GoogleAuth y GoogleDrive
        mock_gauth = mock_GoogleAuth.return_value
        mock_gauth.credentials = MagicMock()
        mock_gauth.access_token_expired = False
        mock_drive = mock_GoogleDrive.return_value

        # Configurar el comportamiento simulado para la autenticación
        mock_gauth.LoadCredentialsFile.return_value = None
        mock_gauth.credentials is None
        mock_gauth.Authorize.return_value = True

        # Ejecutar la función a probar
        drive = authenticate_with_google_drive()

        # Verificar el resultado
        self.assertEqual(drive, mock_drive)


    @patch('myapp.inventario.Classification')
    def test_get_classification(self, mock_Classification):
        # Configurar objeto simulado para Classification
        mock_classification = MagicMock(spec=Classification)
        mock_Classification.objects.filter.return_value.latest.return_value = mock_classification

        # Configurar datos simulados para google_drive_file_id
        google_drive_file_id = "file_id"

        # Ejecutar la función a probar
        classification = get_classification(google_drive_file_id)

        # Verificar el resultado
        self.assertEqual(classification, mock_classification.classification)

    @patch('myapp.inventario.authenticate_with_google_drive')
    @patch('myapp.inventario.File')
    def test_inventario(self, mock_File, mock_authenticate):
        # Configurar objeto simulado para GoogleDrive
        mock_drive = MagicMock()
        mock_authenticate.return_value = mock_drive

        # Configurar objeto simulado para File
        mock_file = MagicMock(spec=File)
        mock_File.objects.create.return_value = mock_file

        # Configurar datos simulados para file_list
        file_list = [
            {"id": "file_id_1", "owners": [{"permissionId": "user_id_1", "emailAddress": "user1@example.com", "displayName": "User 1"}], "title": "file1.txt", "capabilities": {"canEdit": True}, "mimeType": "text/plain", "fileExtension": "txt"},
            {"id": "file_id_2", "owners": [{"permissionId": "user_id_2", "emailAddress": "user2@example.com", "displayName": "User 2"}], "title": "file2.docx", "capabilities": {"canEdit": False}, "mimeType": "application/msword"}
        ]
        mock_drive.ListFile.return_value.GetList.return_value = file_list

        # Ejecutar la función a probar
        inventario()

        # Verificar las interacciones
        mock_File.objects.all.return_value.delete.assert_called_once()
        mock_File.objects.create.assert_called()

if __name__ == '__main__':
    unittest.main()