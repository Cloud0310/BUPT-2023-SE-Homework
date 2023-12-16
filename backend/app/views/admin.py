from flask import Blueprint, request, jsonify, session
from app import db
from app.scheduler import RoomScheduler, room_scheduler_map
from app.utils import check_csrf_token
from app.models import Device, Room, Status

admin_blueprint = Blueprint("admin", __name__)

@admin_blueprint.route("/api/admin/device", methods=["PUT"])
def add_device():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # if not check_csrf_token(request.json.get('csrf_token')):
    #     return jsonify({"error": "CSRF token mismatch"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request data"}), 400

    room = data.get("room")
    public_key = data.get("public_key")

    device = Device(room=room, public_key=public_key)
    db.session.add(device)
    db.session.commit()

    room_scheduler_map[room.id] = RoomScheduler(room.id, 25, 25)

    return jsonify({"room": device.room}), 200

@admin_blueprint.route("/api/admin/device", methods=["DELETE"])
def remove_device():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # if not check_csrf_token(request):
    #     return jsonify({"error": "CSRF token mismatch"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request data"}), 400

    room = data.get("room")

    device = Device.query.filter_by(room=room).first()
    if device:
        db.session.delete(device)
        db.session.commit()
        return jsonify({"room": device.room}), 200
    else:
        return jsonify({"error": "Device not found"}), 404

@admin_blueprint.route("/api/admin/devices", methods=["GET"])
def get_all_devices():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # if not check_csrf_token(request):
    #     return jsonify({"error": "CSRF token mismatch"}), 403

    devices = Device.query.all()
    device_list = [device.room for device in devices]
    return jsonify(device_list), 200