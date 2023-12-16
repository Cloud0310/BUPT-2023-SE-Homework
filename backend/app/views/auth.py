from flask import Blueprint, request, jsonify, session, current_app
from app import db
from app.models import User, Device
from app.scheduler import room_scheduler_map, RoomScheduler

auth_blueprint = Blueprint("auth", __name__)

def generate_csrf_token():
    return "This_is_csrf_token"


@auth_blueprint.route("/api/login", methods=["POST"])
def login():
    if len(room_scheduler_map) == 0:
        for room in Device.query.all():
            room_scheduler_map[room.id] = RoomScheduler(room.id, 25, 25)

    data = request.json

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        session["user_id"] = user.id
        session.permanent = True
        csrf_token = generate_csrf_token()
        session["csrf_token"] = csrf_token
        return jsonify({"username": user.username, "role": user.role, "csrf_token": csrf_token}), 200
    else:
        return jsonify({"error": "Login failed"}), 401

@auth_blueprint.route("/api/logout", methods=["POST"])
def logout():
    if "session" in request.cookies:
        # Clean cookie
        response = jsonify({"message": "Logout successfully"})
        response.delete_cookie("session")

        return response, 204
    else:
        return jsonify({"message": "Not logged in"}), 401