from flask import Blueprint, request, jsonify
from app.models import Device
from app.scheduler import client_remote_map, scheduler
from app.utils import verify_signature

client_blueprint = Blueprint("client", __name__)

@client_blueprint.route("/api/device/client", methods=["POST"])
def handle_client_online():
    if not scheduler.special_initialized:
        for room in Device.query.all():
            scheduler.room_online(room.id, room.public_key)
        scheduler.special_initialized = True

    data = request.json

    remote_addr = request.remote_addr

    room_id = data.get("room_id")
    port = data.get("port")
    unique_id = data.get("unique_id")
    signature = data.get("signature")
    room = Device.query.filter_by(room=room_id).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404

    public_key = room.public_key
    verify_str = str(room_id) + str(unique_id) + str(port)
    if not verify_signature(verify_str, public_key, signature):
        return jsonify({"error": "Signature verification failed"}), 403

    client_remote_map[room.id] = f"http://{remote_addr}:{port}/control"
    scheduler.room_online(room.id, public_key)

    return jsonify({"message": "Online successfully"}), 204