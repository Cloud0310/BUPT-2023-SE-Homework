import math
from flask import Blueprint, request, jsonify, session
from sqlalchemy import desc
from app import db
from app.datamodel import Status, Device
from app.utils import check_csrf_token

room_blueprint = Blueprint("room", __name__)

# 检查用户是否已登录，未登录返回401错误
def check_user_session():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return None

# 获取房间信息
def get_room(room_number):
    return Device.query.filter_by(room=room_number).first()

# 计算电费
def calculate_cost(speed, delta_time):
    cost_rate = 0.5
    speed_to_minutes = {1: 3, 2: 2, 3: 1}
    speed_minutes = speed_to_minutes.get(speed, 1)
    energy_consumed = (delta_time / 60.0) / speed_minutes
    electricity_cost = energy_consumed * cost_rate
    return electricity_cost * 6

# 获取详细账单
def get_detailed_bill(statuses):
    detailed_bill = []
    total_cost = 0
    total_time = 0

    for i in range(len(statuses) - 1):
        if statuses[i].is_on == 0:
            continue
        start_time = statuses[i + 1].last_update
        end_time = statuses[i].last_update
        speed = statuses[i].wind_speed
        temperature = statuses[i].temperature
        sweep = statuses[i].sweep
        delta_time = math.ceil((end_time - start_time).total_seconds())

        electricity_cost = calculate_cost(speed, delta_time)
        total_cost += electricity_cost
        total_time += delta_time
        detailed_bill.append(
            {
                "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "wind_speed": speed,
                "temperature": temperature,
                "sweep": sweep,
                "mode": statuses[i].mode,
                "duration": delta_time,
                "cost": math.ceil(electricity_cost * 100) / 100,
            }
        )

    return detailed_bill, total_cost, total_time

# 处理房间入住请求
@room_blueprint.route("/api/room/check_in", methods=["POST"])
def check_in():
    unauthorized_response = check_user_session()
    if unauthorized_response:
        return unauthorized_response

    data = request.get_json()
    room_number = data.get("room")

    room = get_room(room_number)
    if room:
        return jsonify({"room": room.room}), 200
    else:
        return jsonify({"error": "Room not found"}), 404

# 处理房间退房请求
@room_blueprint.route("/api/room/check_out", methods=["POST"])
def check_out():
    unauthorized_response = check_user_session()
    if unauthorized_response:
        return unauthorized_response

    data = request.get_json()
    room_number = data.get("room")

    room = get_room(room_number)
    if room:
        statuses = (
            Status.query.filter_by(room_id=room.id)
            .order_by(desc(Status.last_update))
            .all()
        )

        detailed_bill, total_cost, total_time = get_detailed_bill(statuses)

        status_to_delete = Status.query.filter_by(room_id=room.id).all()
        for status in status_to_delete:
            db.session.delete(status)

        db.session.commit()

        return (
            jsonify(
                {
                    "room": room.room,
                    "report": {
                        "total_cost": math.ceil(total_cost * 100) / 100,
                        "total_time": total_time,
                        "details": detailed_bill,
                    },
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "Room not found"}), 404
