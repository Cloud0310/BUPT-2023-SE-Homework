import time
from flask import Blueprint, request, jsonify
from app.models import Device
from app.scheduler import client_remote_map, scheduler
from app.utils import verify_signature

client_blueprint = Blueprint("client", __name__)

# 初始化所有房间
def initialize_rooms():
    if not scheduler.special_initialized:
        for room in Device.query.all():
            scheduler.room_online(room.id, room.public_key)
        scheduler.special_initialized = True

# 处理客户端在线请求
def handle_client_online_request(data, remote_addr):
    room_id = data.get("room_id")
    port = data.get("port")
    unique_id = data.get("unique_id")
    signature = data.get("signature")

    # 检查房间是否存在
    room = Device.query.filter_by(room=room_id).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404

    public_key = room.public_key
    # 验证签名
    verify_str = str(room_id) + str(unique_id) + str(port)
    if not verify_signature(verify_str, public_key, signature):
        return jsonify({"error": "Signature verification failed"}), 403

    return room, public_key

# 处理客户端在线请求
@client_blueprint.route("/api/device/client", methods=["POST"])
def handle_client_online():
    initialize_rooms()

    data = request.json
    remote_addr = request.remote_addr

    room, public_key = handle_client_online_request(data, remote_addr)

    client_remote_map[room.id] = f"http://{remote_addr}:{data['port']}/control"
    scheduler.room_online(room.id, public_key)

    return jsonify({"message": "Online successfully"}), 204
