from flask import Blueprint, request, jsonify, session
from app.datamodel import Device
from app.utils import verify_signature
from app.controller import scheduler

control_blueprint = Blueprint("control", __name__)

def add_room_to_queue(room_number_id):
    scheduler.add_room_in_queue(room_number_id)

def remove_room_from_queue(room_number_id):
    scheduler.remove_room_from_queue(room_number_id)

def update_temperature(room_number_id, value):
    scheduler.update_temperature(room_number_id, value)

def update_wind_speed(room_number_id, value):
    scheduler.update_wind_speed(room_number_id, value)

def update_mode(room_number_id, value):
    scheduler.update_mode(room_number_id, value)

def update_sweep(room_number_id, value):
    scheduler.update_sweep(room_number_id, value == "True")

def make_status(room_number_id, operation, value):
    if operation == "start":
        add_room_to_queue(room_number_id)
    elif operation == "stop":
        remove_room_from_queue(room_number_id)
    elif operation == "temperature":
        update_temperature(room_number_id, int(value))
    elif operation == "wind_speed":
        update_wind_speed(room_number_id, int(value))
    elif operation == "mode":
        update_mode(room_number_id, value)
    elif operation == "sweep":
        update_sweep(room_number_id, value)

    return jsonify({"message": "Operation successfully"}), 204

def check_user_session():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return None

@control_blueprint.route("/api/admin/device/<room_id>", methods=["POST"])
def admin_control(room_id):
    unauthorized_response = check_user_session()
    if unauthorized_response:
        return unauthorized_response

    data = request.json
    operation = data.get("operation")
    value = data.get("data")
    room = Device.query.filter_by(room=room_id).first()

    if not room:
        return jsonify({"error": "Room not found"}), 404

    make_status(room.id, operation, value)
    return jsonify({"message": "Operation successfully"}), 204

@control_blueprint.route("/api/device/client/<room_id>", methods=["POST"])
def server_control(room_id):
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
    verify_str = str(operation) + str(unique_id) + str(value) + str(time)
    
    if not verify_signature(verify_str, public_key, signature):
        return jsonify({"error": "Signature verification failed"}), 403

    make_status(room.id, operation, value)
    return jsonify({"message": "Operation successfully"}), 204
