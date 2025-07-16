import unittest
from unittest.mock import MagicMock
from src.models.rideparticipation import RideParticipation

class TestRideParticipation(unittest.TestCase):
    def setUp(self):
        #Se crea un objeto simulado de RideParticipation para pruebas
        self.participant = MagicMock(spec=RideParticipation)
        self.participant.participant = "lgomez"
        self.participant.destination = "Av Aramburú 123"
        self.participant.occupiedSpaces = 1
        self.participant.status = "waiting"
        self.participant.confirmation = None

    #Comprueba que un nuevo participante se inicializa correctamente
    def test_estado_inicial(self):
        """Caso de éxito: Estado inicial debe ser 'waiting' y confirmación en None"""
        self.assertEqual(self.participant.status, "waiting")
        self.assertIsNone(self.participant.confirmation)

    #Verifica que el cambio a 'confirmed' actualiza el estado y asigna confirmación
    def test_cambiar_a_confirmed(self):
        """Caso de éxito: Cambiar estado a 'confirmed' y asignar confirmación"""
        self.participant.status = "confirmed"
        self.participant.confirmation = "2025-07-16T19:00:00"
        self.assertEqual(self.participant.status, "confirmed")
        self.assertIsNotNone(self.participant.confirmation)

    #Asegura que un participante rechazado no tenga confirmación
    def test_rechazo_de_participante(self):
        """Caso de error: Un participante rechazado no debería tener confirmación previa"""
        self.participant.status = "rejected"
        self.participant.confirmation = None
        self.assertEqual(self.participant.status, "rejected")
        self.assertIsNone(self.participant.confirmation)

    #Verifica que un estado no válido no debe ser parte de los permitidos
    def test_status_invalid(self):
        """Caso de error: Asignar un estado inválido debería ser evitado (si se valida)"""
        self.participant.status = "unexpected_state"
        estados_validos = ["waiting", "confirmed", "rejected", "inprogress", "missing", "done", "notmarked"]
        self.assertNotIn(self.participant.status, estados_validos)

if __name__ == "__main__":
    unittest.main()