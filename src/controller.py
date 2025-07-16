from flask import Flask, jsonify, request
from datetime import datetime
from src.models.usuario import User
from src.models.ride import Ride
from src.models.rideparticipation import RideParticipation
from src.data_handler import DataHandler

app = Flask(__name__)
data_handler = DataHandler()

# UTILS 

def find_user(alias):
    return next((u for u in data_handler.users if u.alias == alias), None)

def find_ride(ride_id):
    return next((r for r in data_handler.rides if str(r.id) == str(ride_id)), None)

def find_participant(ride, alias):
    return next((p for p in ride.participants if p.participant == alias), None)

# -- ENDPOINTS ---

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    return jsonify([u.to_dict() for u in data_handler.users])

@app.route("/usuarios/<alias>", methods=["GET"])
def obtener_usuario(alias):
    user = find_user(alias)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user.to_dict())

@app.route("/usuarios/<alias>/rides", methods=["GET"])
def listar_rides_usuario(alias):
    user = find_user(alias)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify([r.to_dict() for r in data_handler.rides if r.driver == alias])

@app.route("/usuarios/<alias>/rides/<ride_id>", methods=["GET"])
def obtener_ride(alias, ride_id):
    ride = find_ride(ride_id)
    if not ride or ride.driver != alias:
        return jsonify({"error": "Ride no encontrado"}), 404

    participantes_detalle = []
    for p in ride.participants:
        stats = {
            "previousRidesTotal": 0,
            "previousRidesCompleted": 0,
            "previousRidesMissing": 0,
            "previousRidesNotMarked": 0,
            "previousRidesRejected": 0
        }
        for r in data_handler.rides:
            for rp in r.participants:
                if rp.participant == p.participant:
                    stats["previousRidesTotal"] += 1
                    if rp.status == "done":
                        stats["previousRidesCompleted"] += 1
                    elif rp.status == "missing":
                        stats["previousRidesMissing"] += 1
                    elif rp.status == "notmarked":
                        stats["previousRidesNotMarked"] += 1
                    elif rp.status == "rejected":
                        stats["previousRidesRejected"] += 1
        participantes_detalle.append({
            "confirmation": p.confirmation,
            "participant": {
                "alias": p.participant,
                **stats
            },
            "destination": p.destination,
            "occupiedSpaces": p.occupiedSpaces,
            "status": p.status
        })

    ride_json = ride.to_dict()
    ride_json["participants"] = participantes_detalle
    return jsonify({"ride": ride_json})

@app.route("/usuarios/<alias>/rides/create", methods=["POST"])
def crear_ride(alias):
    user = find_user(alias)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    data = request.get_json()
    ride_id = len(data_handler.rides) + 1
    ride = Ride(
        ride_id=ride_id,
        ride_date_time=data["rideDateAndTime"],
        final_address=data["finalAddress"],
        allowed_spaces=data["allowedSpaces"],
        driver_alias=alias
    )
    data_handler.rides.append(ride)
    data_handler.save_data()
    return jsonify({"rideId": ride.id}), 201

@app.route("/usuarios/<alias>/rides/<ride_id>/requestToJoin/<participant_alias>", methods=["POST"])
def request_join(alias, ride_id, participant_alias):
    ride = find_ride(ride_id)
    if not ride or ride.driver != alias:
        return jsonify({"error": "Ride no encontrado"}), 404
    if ride.status != "ready":
        return jsonify({"error": "Ride ya fue iniciado"}), 422
    if find_participant(ride, participant_alias):
        return jsonify({"error": "Ya solicitó unirse"}), 422

    user = find_user(participant_alias)
    if not user:
        return jsonify({"error": "Usuario participante no existe"}), 404

    data = request.get_json()
    p = RideParticipation(
        participant_alias,
        destination=data["destination"],
        occupied_spaces=data["occupiedSpaces"]
    )
    ride.participants.append(p)
    data_handler.save_data()
    return jsonify({"message": "Solicitud enviada"}), 200

@app.route("/usuarios/<alias>/rides/<ride_id>/accept/<participant_alias>", methods=["POST"])
def accept_participant(alias, ride_id, participant_alias):
    ride = find_ride(ride_id)
    if not ride or ride.driver != alias:
        return jsonify({"error": "Ride no encontrado"}), 404

    participant = find_participant(ride, participant_alias)
    if not participant:
        return jsonify({"error": "Participante no ha solicitado unirse"}), 404
    if participant.status != "waiting":
        return jsonify({"error": "Ya fue aceptado o rechazado"}), 422

    total_ocupado = sum(p.occupiedSpaces for p in ride.participants if p.status == "confirmed")
    if total_ocupado + participant.occupiedSpaces > ride.allowedSpaces:
        return jsonify({"error": "No hay espacio suficiente"}), 422

    participant.status = "confirmed"
    participant.confirmation = datetime.now().isoformat()
    data_handler.save_data()
    return jsonify({"message": "Participante aceptado"}), 200

@app.route("/usuarios/<alias>/rides/<ride_id>/reject/<participant_alias>", methods=["POST"])
def reject_participant(alias, ride_id, participant_alias):
    ride = find_ride(ride_id)
    if not ride or ride.driver != alias:
        return jsonify({"error": "Ride no encontrado"}), 404

    participant = find_participant(ride, participant_alias)
    if not participant:
        return jsonify({"error": "Participante no encontrado"}), 404

    participant.status = "rejected"
    participant.confirmation = datetime.now().isoformat()
    data_handler.save_data()
    return jsonify({"message": "Participante rechazado"}), 200

@app.route("/usuarios/<alias>/rides/<ride_id>/start", methods=["POST"])
def iniciar_ride(alias, ride_id):
    ride = find_ride(ride_id)
    if not ride or ride.driver != alias:
        return jsonify({"error": "Ride no encontrado"}), 404

    if any(p.status not in ["rejected", "confirmed"] for p in ride.participants):
        return jsonify({"error": "Hay participantes aún en estado waiting"}), 422

    for p in ride.participants:
        if p.status == "confirmed":
            p.status = "inprogress"
        elif p.status == "rejected":
            continue
        else:
            p.status = "missing"
    ride.status = "inprogress"
    data_handler.save_data()
    return jsonify({"message": "Ride iniciado"}), 200

@app.route("/usuarios/<alias>/rides/<ride_id>/end", methods=["POST"])
def terminar_ride(alias, ride_id):
    ride = find_ride(ride_id)
    if not ride or ride.driver != alias:
        return jsonify({"error": "Ride no encontrado"}), 404

    for p in ride.participants:
        if p.status in ["inprogress", "confirmed"]:
            p.status = "notmarked"
    ride.status = "done"
    data_handler.save_data()
    return jsonify({"message": "Ride finalizado"}), 200

@app.route("/usuarios/<alias>/rides/<ride_id>/unloadParticipant", methods=["POST"])
def bajar_participante(alias, ride_id):
    ride = find_ride(ride_id)
    if not ride:
        return jsonify({"error": "Ride no encontrado"}), 404

    participant = find_participant(ride, alias)
    if not participant:
        return jsonify({"error": "Participante no existe en el ride"}), 404
    if participant.status != "inprogress":
        return jsonify({"error": "No está en progreso"}), 422

    participant.status = "done"
    data_handler.save_data()
    return jsonify({"message": "Participante bajado"}), 200

@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    data = request.get_json()
    if find_user(data["alias"]):
        return jsonify({"error": "Usuario ya existe"}), 422
    new_user = User(data["alias"], data["name"], data.get("carPlate"))
    data_handler.users.append(new_user)
    data_handler.save_data()
    return jsonify({"message": "Usuario creado"}), 201

if __name__ == '__main__':
    app.run(debug=True)
