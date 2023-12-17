from app import db
from datetime import datetime


# 每个 class 代表一张表
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 将id定义为主键
    room = db.Column(db.String(255), unique=True, nullable=False)  # room为候选键，不为空
    public_key = db.Column(db.String(4096), nullable=False)


# 储存用户信息
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # AC admin, checkout, manager


# 设备状态信息
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)  # 房间号
    temperature = db.Column(db.Integer, nullable=False)  # 温度
    wind_speed = db.Column(db.Integer, nullable=False)  # 风速
    mode = db.Column(db.String(255), nullable=False)  # 模式
    sweep = db.Column(db.Boolean, nullable=False)  # 是否摆风
    is_on = db.Column(db.Boolean, nullable=False)  # 是否开机
    last_update = db.Column(db.DateTime, nullable=False)  # 状态改变时间
