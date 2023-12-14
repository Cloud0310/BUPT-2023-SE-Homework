from app import db
from datetime import datetime

"""Note: Every class represents a table."""

# Device information
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(255), unique=True, nullable=False)
    public_key = db.Column(db.String(4096), nullable=False)


# Record user's information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


# Record room's information
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.relationship(
        "Status", backref="room", lazy=True
    )


# Record device's status
class Status(db.Model):
    room_id = db.Column(
        db.Integer, db.ForeignKey("room.id"), primary_key=True, nullable=False
    )
    temperature = db.Column(db.Integer, nullable=False)  # Temperature
    wind_speed = db.Column(db.Integer, nullable=False)  # Wind speed
    mode = db.Column(db.String(255), nullable=False)  # Mode
    sweep = db.Column(db.Boolean, nullable=False)  # Whether to swing
    is_on = db.Column(db.Boolean, nullable=False)  # Whether to turn on
    last_update = db.Column(db.DateTime, nullable=False)  # Last update time
