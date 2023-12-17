from flask import Blueprint, request, jsonify, session, current_app
from app import db
from werkzeug.security import check_password_hash

from app.models import User, Device  # 从数据库处理文件中获取数据
from app.scheduler import scheduler

# 创建一个蓝图对象
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

    # 从数据库中获取用户信息
    user = User.query.filter_by(username=username).first()  # 这里需要修改

    # 将输入内容进行验证
    # if user and check_password_hash(user.password_hash, password):  # 这里需要修改
    if user and user.password == password:
        # 登录成功
        session["user_id"] = user.id
        session.permanent = True  # 设置会话为永久有效
        csrf_token = generate_csrf_token()  # 生成 CSRF token
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
    # 检查用户是否已登录
    if "session" in request.cookies:
        # 存在 session，则代表用户已登录，可执行注销操作

        # 清除 Cookie
        response = jsonify({"message": "Logout successfully"})
        response.delete_cookie("session")

        return response, 204
    else:
        # 用户未登录
        return jsonify({"message": "Not logged in"}), 401


def generate_csrf_token():
    return "your_generated_csrf_token"
