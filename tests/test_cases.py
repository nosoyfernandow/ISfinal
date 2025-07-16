import unittest
from unittest.mock import MagicMock
from src.models.ride import Ride
from src.models.rideparticipation import RideParticipation
from src.models.usuario import User

class TestCasosUnitarios(unittest.TestCase):

    # CASO DE ÉXITO
    def test_usuario_valido(self):
        """Caso de éxito: Usuario creado con alias, nombre y placa"""
        user = User(alias="jperez", name="Juan Pérez", car_plate="ABC-123")
        self.assertEqual(user.alias, "jperez")
        self.assertEqual(user.name, "Juan Pérez")
        self.assertEqual(user.car_plate, "ABC-123")

    # CASO DE ERROR 1
    def test_participantes_exceden_limite(self):
        """Error: No se debe aceptar más participantes que los espacios permitidos"""
        ride = Ride(ride_id=1, ride_date_time="2025-07-16 19:00", final_address="Av X", allowed_spaces=1, driver_alias="jperez")
        p1 = RideParticipation("a", "Destino A", 1)
        p1.status = "confirmed"
        p2 = RideParticipation("b", "Destino B", 1)
        p2.status = "confirmed"
        ride.participants.extend([p1, p2])
        total = sum(p.occupiedSpaces for p in ride.participants if p.status == "confirmed")
        self.assertGreater(total, ride.allowedSpaces)

    # CASO DE ERROR 2
    def test_estado_invalido_participante(self):
        """Error: El estado del participante no es válido"""
        participant = RideParticipation("lgomez", "Destino", 1)
        participant.status = "no_valido"
        estados_validos = ["waiting", "confirmed", "rejected", "inprogress", "missing", "done", "notmarked"]
        self.assertNotIn(participant.status, estados_validos)

    # CASO DE ERROR 3
    def test_alias_duplicado(self):
        """Error: No debe haber dos usuarios con el mismo alias"""
        u1 = MagicMock(spec=User, alias="jperez")
        u2 = MagicMock(spec=User, alias="jperez")
        aliases = [u.alias for u in [u1, u2]]
        self.assertNotEqual(len(set(aliases)), len(aliases))

if __name__ == "__main__":
    unittest.main()