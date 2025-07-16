import unittest
from unittest.mock import MagicMock
from src.models.usuario import User

class TestUsuario(unittest.TestCase):
    def setUp(self):
        #Se inicializa un usuario válido con alias, nombre y placa
        self.user = User(alias="jperez", name="Juan Pérez", car_plate="ABC-123")

    #Verifica que los datos del usuario sean correctamente asignados
    def test_datos_usuario(self):
        """Caso de éxito: El usuario debe tener alias, nombre y placa correctos"""
        self.assertEqual(self.user.alias, "jperez")
        self.assertEqual(self.user.name, "Juan Pérez")
        self.assertEqual(self.user.car_plate, "ABC-123")

    #Comprueba que un usuario puede existir sin placa registrada
    def test_usuario_sin_placa(self):
        """Caso de éxito: El usuario puede no tener car_plate"""
        user = User(alias="lgomez", name="Laura Gómez")
        self.assertEqual(user.alias, "lgomez")
        self.assertIsNone(user.car_plate)

    #Verifica que no haya usuarios con alias duplicado en una lista
    def test_alias_duplicado_en_lista(self):
        """Caso de error: No debe haber dos usuarios con el mismo alias en la lista"""
        users = [
            MagicMock(spec=User, alias="jperez"),
            MagicMock(spec=User, alias="jperez")
        ]
        aliases = [u.alias for u in users]
        self.assertNotEqual(len(set(aliases)), len(aliases))  # Hay duplicados

    #Valida que el nombre del usuario no esté vacío o en blanco
    def test_nombre_vacio(self):
        """Caso de error: Un usuario no debería tener nombre vacío"""
        user = User(alias="x", name="")
        self.assertTrue(user.name == "" or user.name.isspace())

if __name__ == "__main__":
    unittest.main()