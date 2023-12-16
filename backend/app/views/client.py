import time
from flask import Blueprint, request, jsonify
from app.models import Device, Status
from app import db
from datetime import datetime
from app.scheduler import room_scheduler_map, RoomScheduler
from app.utils import generate_timestamp_id, verify_signature

client_blueprint = Blueprint("client", __name__)

client_remote_map = {}

# Judge whether the client is online
@client_blueprint.route("/api/device/client", methods=["POST"])
def handle_client_online():
    if len(room_scheduler_map) == 0:
        for room in Device.query.all():
            room_scheduler_map[room.id] = RoomScheduler(room.id, 25, 25)

    data = request.json

    room_id = data.get("room_id")
    port = data.get("port")
    unique_id = data.get("unique_id")
    signature = data.get("signature")

    # Initial the room scheduler
    # Check whether the room is in the database
    room = Device.query.filter_by(room=room_id).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404

    public_key = room.public_key

    verify_str = str(room_id) + str(unique_id) + str(port)
    if not verify_signature(verify_str, public_key, signature):
        return jsonify({"error": "Signature verification failed"}), 403

    # Update the room scheduler
    selected_room = room_scheduler_map[room.id]
    selected_room.last_update_temperature = time.time()

    status_id = generate_timestamp_id()
    status = Status(
        room_id=room_id,
        temperature=25,
        wind_speed=2,
        mode="cool",
        sweep=False,
        is_on=False,
        last_update=datetime.utcnow(),
    )
    db.session.add(status)
    db.session.commit()

    return jsonify({"message": "Online successfully"}), 204