from unittest.mock import patch
from django.test import TestCase
from myapp.inventario import get_visibility

class GetVisibilityTests(TestCase):
    @patch('myapp.inventario.authenticate_with_google_drive')
    def test_visibility_anyone_with_link(self, mock_authenticate):
        # Simulamos un permiso con "anyoneWithLink"
        permissions = [{"id": "anyoneWithLink"}, {"id": "user123"}]

        # Configuramos el comportamiento del mock para authenticate_with_google_drive
        mock_drive = mock_authenticate.return_value
        mock_drive.CreateFile.return_value.GetPermissions.return_value = permissions

        result = get_visibility(None)  # Pasamos None ya que el argumento no se utiliza en la prueba
        self.assertEqual(result, "anyoneWithLink")

    @patch('myapp.inventario.authenticate_with_google_drive')
    def test_visibility_restricted(self, mock_authenticate):
        # Simulamos permisos sin "anyoneWithLink"
        permissions = [{"id": "user123"}, {"id": "user456"}]

        # Configuramos el comportamiento del mock para authenticate_with_google_drive
        mock_drive = mock_authenticate.return_value
        mock_drive.CreateFile.return_value.GetPermissions.return_value = permissions

        result = get_visibility(None)
        self.assertEqual(result, "Restricted")

    @patch('myapp.inventario.authenticate_with_google_drive')
    def test_visibility_default(self, mock_authenticate):
        # Simulamos permisos vacíos
        permissions = []

        # Configuramos el comportamiento del mock para authenticate_with_google_drive
        mock_drive = mock_authenticate.return_value
        mock_drive.CreateFile.return_value.GetPermissions.return_value = permissions

        result = get_visibility(None)
        self.assertEqual(result, "Restricted")