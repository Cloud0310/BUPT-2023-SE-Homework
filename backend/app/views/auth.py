from flask import Blueprint, request, jsonify, session
from app.models import User, Device
from app.scheduler import scheduler

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/api/login", methods=["POST"])
def login():
    if not scheduler.special_initialized:
        for room in Device.query.all():
            scheduler.room_online(room.id, room.public_key)
        scheduler.special_initialized = True

    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session["user_id"] = user.id
        session.permanent = True
        csrf_token = generate_csrf_token()
        session["csrf_token"] = csrf_token
        return (
            jsonify(
                {"username": user.username, "role": user.role, "csrf_token": csrf_token}
            ),
            200,
        )
    else:
        return jsonify({"error": "Login failed"}), 401


@auth_blueprint.route("/api/logout", methods=["POST"])
def logout():
    if "session" in request.cookies:
        response = jsonify({"message": "Logout successfully"})
        response.delete_cookie("session")
        return response, 204
    else:
        return jsonify({"message": "Not logged in"}), 401


def generate_csrf_token():
    return "This_is_your_csrf_token"