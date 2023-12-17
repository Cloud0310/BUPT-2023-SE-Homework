# backend/app/views/room.py
import math

from flask import Blueprint, request, jsonify, session
from sqlalchemy import desc

from app import db
from app.models import Status, Device
from app.utils import check_csrf_token

room_blueprint = Blueprint("room", __name__)


@room_blueprint.route("/api/room/check_in", methods=["POST"])
def check_in():
    # 检查用户是否已登录
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # # 检查 CSRF token
    # if not check_csrf_token(request):
    #     return jsonify({'error': 'CSRF token mismatch'}), 403

    data = request.get_json()
    room_id = data.get("room")

    # 根据实际情况处理房间入住逻辑
    room = Device.query.filter_by(room=room_id).first()
    if room:
        return jsonify({"room": room.room}), 200
    else:
        return jsonify({"error": "Room not found"}), 404


@room_blueprint.route("/api/room/check_out", methods=["POST"])
def check_out():
    # 检查用户是否已登录
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # # 检查 CSRF token
    # if not check_csrf_token(request):
    #     return jsonify({'error': 'CSRF token mismatch'}), 403

    data = request.get_json()
    room_number = data.get("room")

    # 根据实际情况处理房间退房逻辑
    room = Device.query.filter_by(room=room_number).first()
    if room:
        statuses = (
            Status.query.filter_by(room_id=room.id)
            .order_by(desc(Status.last_update))
            .all()
        )

        total_cost = 0  # 总费用
        total_time = 0
        detailed_bill = []  # 详细账单
        # 计算费用
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

        # 更新房间状态等信息，删除这一阶段所有的记录
        status_to_delete = Status.query.filter_by(room_id=room.id).all()
        for status in status_to_delete:
            db.session.delete(status)

        # 提交修改
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


def calculate_cost(speed, delta_time):
    # 设置费率
    cost_rate = 0.5

    # 设置不同风速下每度电的运行时间
    speed_to_minutes = {1: 3, 2: 2, 3: 1}

    # 风速对应的每度电运行时间
    speed_minutes = speed_to_minutes.get(speed, 1)

    # 计算用电量
    energy_consumed = (delta_time / 60.0) / speed_minutes

    # 计算电费
    electricity_cost = energy_consumed * cost_rate

    return electricity_cost * 6
