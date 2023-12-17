from flask import Blueprint, request, jsonify, session
from app.datamodel import Status, Device
from app import db
from sqlalchemy import desc

query_blueprint = Blueprint("query", __name__)

# 检查用户会话，如果未授权则返回401错误
def check_user_session():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return None

# 获取指定房间的状态
def get_room_status(room_id):
    status = (
        Status.query.filter_by(room_id=room_id)
        .order_by(desc(Status.last_update))
        .first()
    )

    return status

# 处理单个房间状态请求
@query_blueprint.route("/api/status/<room_id>", methods=["GET"])
def get_status(room_id):
    unauthorized_response = check_user_session()
    if unauthorized_response:
        return unauthorized_response

    room = Device.query.filter_by(room=room_id).first()
    if room:
        status = get_room_status(room.id)

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

# 获取全部房间的状态
@query_blueprint.route("/api/status", methods=["GET"])
def get_all_status():
    unauthorized_response = check_user_session()
    if unauthorized_response:
        return unauthorized_response

    all_room = Device.query.all()
    response_data = []

    for room in all_room:
        status = get_room_status(room.id)
        room_data = {
            "room": room.room,
            "is_on": status.is_on if status else False,
        }
        response_data.append(room_data)

    return jsonify(response_data), 200
