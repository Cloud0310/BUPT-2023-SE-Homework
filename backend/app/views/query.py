# 处理数据查询文件
from flask import Blueprint, request, jsonify, session
from app.models import Status, Device
from app import db
from sqlalchemy import desc


query_blueprint = Blueprint("query", __name__)


# 获得某个房间的状态
@query_blueprint.route("/api/status/<room_id>", methods=["GET"])
def get_status(room_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    room = Device.query.filter_by(room=room_id).first()
    if room:
        status = (
            Status.query.filter_by(room_id=room.id)
            .order_by(desc(Status.last_update))
            .first()
        )

        if status:
            response_data = {
                "room": room.room,
                "temperature": status.temperature,
                "wind_speed": status.wind_speed,
                "mode": status.mode,
                "sweep": status.sweep,
                "is_on": status.is_on,
                "last_update": status.last_update.isoformat(),
            }
            return jsonify(response_data), 200
        else:
            response_data = {
                "room": room.room,
                "temperature": 26,
                "wind_speed": 1,
                "mode": "cool",
                "sweep": False,
                "is_on": False,
                "last_update": "-1",
            }
            return jsonify(response_data), 200
    else:
        return jsonify({"error": "Room not found"}), 404


# 获得全部房间的状态
@query_blueprint.route("/api/status", methods=["GET"])
def get_all_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    all_room = Device.query.all()
    response_data = []
    for room in all_room:
        status = (
            Status.query.filter_by(room_id=room.id)
            .order_by(desc(Status.last_update))
            .first()
        )
        if status:
            room_data = {
                "room": room.room,
                "is_on": status.is_on,
            }
            response_data.append(room_data)
        else:
            room_data = {
                "room": room.room,
                "is_on": False,
            }
            response_data.append(room_data)
    return jsonify(response_data), 200
