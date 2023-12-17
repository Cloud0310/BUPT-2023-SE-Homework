from flask import Blueprint, request, jsonify, session
from app import db
from app.scheduler import scheduler
from app.utils import check_csrf_token

from app.models import Device, Status  # 获取关于设备的信息

admin_blueprint = Blueprint("admin", __name__)


@admin_blueprint.route("/api/admin/device", methods=["PUT"])
def add_device():
    # 检查用户是否已登录
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # # 检查 CSRF token
    # if not check_csrf_token(request):
    #     return jsonify({"error": "CSRF token mismatch"}), 403

    data = request.get_json()

    room = data.get("room")
    public_key = data.get("public_key")

    # 根据实际情况将设备信息保存到数据库中
    device = Device(room=room, public_key=public_key)
    db.session.add(device)
    db.session.commit()

    scheduler.room_online(device.id, public_key)

    return jsonify({"room": device.room}), 200


@admin_blueprint.route("/api/admin/device", methods=["DELETE"])
def remove_device():
    # 检查用户是否已登录
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # 检查 CSRF token
    if not check_csrf_token(request):
        return jsonify({"error": "CSRF token mismatch"}), 403

    # 获取删除相关信息
    data = request.get_json()

    room = data.get("room")

    # 根据实际情况从数据库中删除设备信息
    device = Device.query.filter_by(room=room).first()  # 这里只是示例
    if device:
        db.session.delete(device)
        db.session.commit()
        return jsonify({"room": device.room}), 200
    else:
        return jsonify({"error": "Device not found"}), 404


@admin_blueprint.route("/api/admin/devices", methods=["GET"])
def get_all_devices():
    # 检查用户是否已登录
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # # 检查 CSRF token
    # if not check_csrf_token(request):
    #     return jsonify({"error": "CSRF token mismatch"}), 403

    # 根据实际情况从数据库中获取所有设备信息
    devices = Device.query.all()
    device_list = [device.room for device in devices]

    return jsonify(device_list), 200
