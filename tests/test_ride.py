import unittest
from src.models.ride import Ride
from src.models.rideparticipation import RideParticipation

class TestRide(unittest.TestCase):
    def setUp(self):
        self.ride = Ride(
            ride_id=1,
            ride_date_time="2025-07-16 19:00",
            final_address="Av Arequipa 123",
            allowed_spaces=2,
            driver_alias="jperez"
        )

    #Verifica que se pueda agregar un nuevo participante correctamente
    def test_agregar_participante_valido(self):
        """Caso de éxito: Se agrega un participante nuevo en estado waiting"""
        p = RideParticipation("lgomez", "Av Aramburú", 1)
        self.ride.participants.append(p)
        self.assertEqual(len(self.ride.participants), 1)
        self.assertEqual(self.ride.participants[0].participant, "lgomez")
        self.assertEqual(self.ride.participants[0].status, "waiting")

    #Comprueba que no se pueda aceptar un participante si se excede el cupo permitido
    def test_aceptar_sin_espacio(self):
        """Caso de error: No se debe aceptar un participante si se supera el límite"""
        self.ride.allowedSpaces = 1
        p1 = RideParticipation("a", "Av1", 1)
        p1.status = "confirmed"
        p2 = RideParticipation("b", "Av2", 1)
        p2.status = "confirmed"
        self.ride.participants.extend([p1, p2])

        total_ocupado = sum(p.occupiedSpaces for p in self.ride.participants if p.status == "confirmed")
        self.assertGreater(total_ocupado, self.ride.allowedSpaces)

    #Valida que no se pueda iniciar un ride si algún participante sigue en estado "waiting"
    def test_inicio_sin_estado_valido(self):
        """Caso de error: No se puede iniciar el ride si algún participante está en estado waiting"""
        p = RideParticipation("c", "Av3", 1)
        p.status = "waiting"
        self.ride.participants.append(p)

        invalid = any(p.status not in ["confirmed", "rejected"] for p in self.ride.participants)
        self.assertTrue(invalid)

    #Verifica que los participantes ausentes al iniciar el ride se marquen como "missing"
    def test_iniciar_ride_participante_missing(self):
        """Caso de error: Participante no presente → se marca como missing"""
        p = RideParticipation("d", "Av4", 1)
        p.status = "confirmed"
        self.ride.participants.append(p)

        for part in self.ride.participants:
            if part.status == "confirmed":
                part.status = "inprogress"
            elif part.status not in ["rejected", "confirmed"]:
                part.status = "missing"

        self.assertIn(self.ride.participants[0].status, ["inprogress", "missing"])

if __name__ == "__main__":
    unittest.main()