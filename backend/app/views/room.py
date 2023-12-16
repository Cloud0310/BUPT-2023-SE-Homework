import math
from flask import Blueprint, request, jsonify, session
from sqlalchemy import desc
from app import db
from app.models import Status, Device

room_blueprint = Blueprint("room", __name__)


@room_blueprint.route("/api/room/check_in", methods=["POST"])
def check_in():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    room_id = data.get("room")
    room = Device.query.filter_by(room=room_id).first()
    if room:
        pass
        return jsonify({"room": room.room}), 200
    else:
        return jsonify({"error": "Room not found"}), 404


@room_blueprint.route("/api/room/check_out", methods=["POST"])
def check_out():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    room_number = data.get("room")

    room = Device.query.filter_by(room=room_number).first()
    if room:
        statuses = Status.query.filter_by(room_id=room.id).order_by(desc(Status.last_update)).all()

        total_cost = 0
        total_time = 0
        detailed_bill = []
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
            detailed_bill.append({
                "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "wind_speed": speed,
                "temperature": temperature,
                "sweep": sweep,
                "mode": statuses[i].mode,
                "duration": delta_time,
                "cost": math.ceil(electricity_cost * 100) / 100
            })

        # Update the room status
        status_to_delete = Status.query.filter_by(room_id=room.id).all()
        for status in status_to_delete:
            db.session.delete(status)

        db.session.commit()

        return jsonify({"room": room.room, "report": {
            "total_cost": math.ceil(total_cost * 100) / 100,
            "total_time": total_time,
            "details": detailed_bill
        }}), 200
    else:
        return jsonify({"error": "Room not found"}), 404


def calculate_cost(speed, delta_time):
    # Set the cost rate
    cost_rate = 0.5

    # Set the speed to minutes map
    speed_to_minutes = {1: 3, 2: 2, 3: 1}

    # Set the default speed
    speed_minutes = speed_to_minutes.get(speed, 1)

    energy_consumed = (delta_time / 60.0) / speed_minutes
    electricity_cost = energy_consumed * cost_rate

    return electricity_cost