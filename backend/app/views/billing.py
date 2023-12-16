from flask import Blueprint, request, jsonify
from app.models import Status
from datetime import datetime
from sqlalchemy import desc
from flask_cors import CORS

billing_blueprint = Blueprint("billing", __name__)
CORS(billing_blueprint)

# Generate bill
@billing_blueprint.route("/billing", methods=["POST"])
def generate_bill():
    data = request.json

    room_id = data.get("room_id")

    # Query all related records
    statuses = (
        Status.query.filter_by(room_id=room_id).order_by(desc(Status.last_update)).all()
    )

    total_cost = 0
    detailed_bill = []
    # Calculate cost
    for i in range(len(statuses) - 1):
        start_time = statuses[i].last_update
        end_time = statuses[i + 1].last_update
        speed = statuses[i].wind_speed
        temperature = statuses[i].temperature
        sweep = statuses[i].sweep

        electricity_cost = calculate_cost(start_time, end_time, speed)
        total_cost += electricity_cost
        segment_info = {
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "speed": speed,
            "temperature": temperature,
            "sweep": sweep,
            "electricity_cost": electricity_cost,
        }

    return (
        jsonify(
            {
                "room_id": room_id,
                "total_cost": total_cost,
                "detailed_bill": detailed_bill,
            }
        ),
        200,
    )


# Calculate cost
def calculate_cost(start_time, end_time, speed):
    cost_rate = 0.5
    # Set the time for each degree of wind speed
    speed_to_minutes = {1: 3, 2: 2, 3: 1}
    # Calculate the time difference
    delta_time = (end_time - start_time).total_seconds() / 60.0
    # Calculate the electricity consumption
    speed_minutes = speed_to_minutes.get(speed, 0)
    # Calculate the electricity consumption
    energy_consumed = delta_time / speed_minutes

    # Calculate the cost
    electricity_cost = energy_consumed * cost_rate
    return electricity_cost
