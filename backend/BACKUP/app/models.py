from app import db
from datetime import datetime


# 每个 class 代表一张表
# 设备信息
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 将id定义为主键
    room = db.Column(db.String(255), unique=True, nullable=False)  # room为候选键，不为空
    public_key = db.Column(db.String(4096), nullable=False)  #


# 暂且用来记录空调状态的改变
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)  #
    room = db.Column(db.String(255), nullable=False)
    operation = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    unique_id = db.Column(db.String(16), nullable=False, unique=True)
    signature = db.Column(db.String(255), nullable=False)  # 数字签名


# 储存用户信息
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


# 储存房间信息
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(10), unique=True, nullable=False)
    status = db.relationship("Status", backref="room", lazy=True)


# 设备状态信息
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Integer, nullable=False)
    mode = db.Column(db.String(255), nullable=False)
    sweep = db.Column(db.Boolean, nullable=False)
    is_on = db.Column(db.Boolean, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False)
