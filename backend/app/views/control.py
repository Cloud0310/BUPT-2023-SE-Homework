from flask import Blueprint, request, jsonify, session
from app.models import Device
from app.utils import verify_signature
from app.scheduler import scheduler

control_blueprint = Blueprint("control", __name__)


def make_status(room_number_id, operation, value):
    if operation == "start":
        scheduler.add_room_in_queue(room_number_id)
    if operation == "stop":
        scheduler.remove_room_from_queue(room_number_id)
    if operation == "temperature":
        scheduler.update_temperature(room_number_id, int(value))
    if operation == "wind_speed":
        scheduler.update_wind_speed(room_number_id, int(value))
    if operation == "mode":
        scheduler.update_mode(room_number_id, value)
    if operation == "sweep":
        scheduler.update_sweep(room_number_id, value == "True")

    return jsonify({"message": "Operation successfully"}), 204


@control_blueprint.route("/api/admin/device/<room_id>", methods=["POST"])
def admin_control(room_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    operation = data.get("operation")
    room = Device.query.filter_by(room=room_id).first()
    value = data.get("data")

    return make_status(room.id, operation, value)


@control_blueprint.route("/api/device/client/<room_id>", methods=["POST"])
def server_control(room_id):
    """
    Server Operations for AC
    """
    data = request.json

    operation = data.get("operation")
    value = data.get("data")
    time = data.get("time")
    unique_id = data.get("unique_id")
    signature = data.get("signature")

    room = Device.query.filter_by(room=room_id).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404

    public_key = room.public_key
    # 验证签名
    verify_str = str(operation) + str(unique_id) + str(value) + str(time)
    if not verify_signature(verify_str, public_key, signature):
        return jsonify({"error": "Signature verification failed"}), 403

    return make_status(room.id, operation, value)
