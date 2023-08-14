import unittest
from unittest.mock import patch, MagicMock
from myapp.models import File, Classification, User
from myapp.cambiar_visibilidad import get_files_to_remove_permission, main

class TestCambiarVisibilidad(unittest.TestCase):
    def setUp(self):
        # Crear objetos simulados (MagicMock) para User y File
        self.user_mock = MagicMock(spec=User)
        self.file_mock = MagicMock(spec=File)

    def test_get_files_to_remove_permission(self):
        # Configurar el objeto simulado File para retornar datos específicos
        self.file_mock.google_drive_file_id = "file_id"
        self.file_mock.visibility = "anyoneWithLink"
        self.file_mock.can_edit = True

        # Configurar el objeto simulado User para retornar datos específicos
        self.user_mock.google_drive_user_id = "user_id"

        # Mockear el método filter de File para que retorne el objeto simulado File
        with patch('myapp.models.File.objects.filter') as mock_file_filter:
            mock_file_filter.return_value.first.return_value = self.file_mock

            # Ejecutar la función a probar
            files_to_remove_permission = get_files_to_remove_permission()

        # Verificar los resultados de la función
        self.assertEqual(files_to_remove_permission, ["file_id"])

    @patch('myapp.cambiar_visibilidad.authenticate_with_google_drive')
    def test_main(self, mock_authenticate):
        # Configurar el objeto simulado Drive para retornar datos específicos
        drive_mock = MagicMock()
        mock_authenticate.return_value = drive_mock

        # Configurar el objeto simulado File para retornar datos específicos
        self.file_mock.google_drive_file_id = "file_id"

        # Configurar el comportamiento simulado para GetPermissions
        permission_mock = {"id": "anyoneWithLink"}
        drive_mock.CreateFile.return_value.GetPermissions.return_value = [permission_mock]

        # Mockear el método filter de File para que retorne el objeto simulado File
        with patch('myapp.models.File.objects.filter') as mock_file_filter:
            mock_file_filter.return_value.first.return_value = self.file_mock

            # Ejecutar la función a probar
            main()

        # Verificar las interacciones
        drive_mock.CreateFile.return_value.DeletePermission.assert_called_once_with("anyoneWithLink")

if __name__ == '__main__':
    unittest.main()

# python manage.py test myapp.tests.test_cambiar_visibilidad