from app import db
from datetime import datetime

"""
Hint: models.py is a file that contains all the database models for the app.
"""

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def init_status():
    status = Status.query.all()
    if len(status) == 0:
        for i in range(1, 11):
            new_status = Status(room_id=i, temperature=26, wind_speed=0, mode="cold", sweep=False, is_on=False, last_update=datetime.now())
            db.session.add(new_status)
        db.session.commit()

# Record device's status
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Integer, nullable=False)
    mode = db.Column(db.String(255), nullable=False)
    sweep = db.Column(db.Boolean, nullable=False)
    is_on = db.Column(db.Boolean, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False)


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
    role = db.Column(db.String(10), nullable=False)