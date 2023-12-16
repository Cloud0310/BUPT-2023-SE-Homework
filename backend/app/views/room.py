from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Room, Status
from app.utils import check_csrf_token
from flask_cors import CORS

room_blueprint = Blueprint("room", __name__)
CORS(room_blueprint)

@room_blueprint.route("/room/check_in", methods=["POST"])
def check_in():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    room_id = data.get("room")

    room = Room.query.filter_by(id=room_id).first()
    if room:
        # Check in logic
        pass
        return jsonify({"room": room.id}), 200
    else:
        return jsonify({"error": "Room not found"}), 404

@room_blueprint.route("/room/check_out", methods=["POST"])
def check_out():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    room_number = data.get("room")

    room = Room.query.filter_by(id=room_number).first()
    if room:
        # Check out logic
        pass
        report_data = generate_report(room)
        return jsonify({"room": room.number, "report": report_data}), 200
    else:
        return jsonify({"error": "Room not found"}), 404

def generate_report(room):
    # Generate report logic
    pass
    return {}