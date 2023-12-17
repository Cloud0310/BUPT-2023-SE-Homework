from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User, Device
from app.scheduler import scheduler

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/api/login", methods=["POST"])
def login():
    initialize_special_scheduler()

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

    return jsonify({"error": "登录失败"}), 401

@auth_blueprint.route("/api/logout", methods=["POST"])
def logout():
    if is_user_logged_in():
        response = jsonify({"message": "注销成功"})
        response.delete_cookie("session")
        return response, 204

    return jsonify({"message": "未登录"}), 401

def initialize_special_scheduler():
    if not scheduler.special_initialized:
        for room in Device.query.all():
            scheduler.room_online(room.id, room.public_key)
        scheduler.special_initialized = True

def is_user_logged_in():
    return "session" in request.cookies

def generate_csrf_token():
    return "your_generated_csrf_token"
