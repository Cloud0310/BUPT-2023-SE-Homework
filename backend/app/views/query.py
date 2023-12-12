from flask import Blueprint, request, jsonify
from app.models import Room, Status
from app import db
from sqlalchemy import desc

query_blueprint = Blueprint("query", __name__)

@query_blueprint.route("/status/<room_id>", methods=["GET"])
def get_status(room_id):
    room = Room.query.filter_by(numbers=room_id).first()
    if room:
        status = Status.query.filter_by(room_id=room.id).order_by(desc(Status.last_update)).first()
        if status:
            response_data = {
                "room": room.id,
                "temperature": status.temperature,
                "wind_speed": status.wind_speed,
                "mode": status.mode,
                "sweep": status.sweep,
                "is_on": status.is_on,
                "last_update": status.last_update.isoformat(),
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "Status not found"}), 404
    else:
        return jsonify({"error": "Room not found"}), 404

@query_blueprint.route("/status", methods=["GET"])
def get_all_status():
    rooms = Room.query.all()
    response_data = []
    for room in rooms:
        status = (
            Status.query.filter_by(room_id=room.id)
            .order_by(desc(Status.last_update))
            .first()
        )
        if status:
            room_data = {
                "room": room.id,
                "is_on": status.is_on,
            }
            response_data.append(room_data)
    return jsonify(response_data), 200