from flask import Blueprint, request, jsonify, session, Flask
from jwt.exceptions import DecodeError
import uuid
import jwt
import sqlite3
import threading
import datetime

api_bp = Blueprint('views', __name__)
api_bp.secret_key = "ilovebupt"

"""
Database Operation [Waiting for development...]
"""
# connect to SQLite database
conn = sqlite3.connect('../db/buptse.db')
cursor = conn.cursor()

# create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS records
                  (id TEXT PRIMARY KEY, room TEXT)''')

# create a thread-local storage object
local_storage = threading.local()


def get_db_connection():
    if not hasattr(local_storage, 'connection'):
        local_storage.connection = sqlite3.connect('../db/buptse.db')
    return local_storage.connection


def cleanup_db_connection(exception=None):
    if hasattr(local_storage, 'connection'):
        local_storage.connection.close()


def check_auth():
    """token = session.get('token')
    if token:
        try:
            decoded_token = jwt.decode(token, "ilovebupt", algorithms=['HS256'])
            if decoded_token.get('username') == 'admin':
                return True
        except DecodeError:
            pass
    return False"""
    return True # In order to test, we just return True


def unauthorized():
    return jsonify({'error': 'OH! FUCK! Unauthorized Access!'}), 401


# 1. login route
@api_bp.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if username == 'admin' and password == 'admin':
        # generate JWT token
        token = jwt.encode({'username': username}, "ilovebupt") # hard code first
        # save token to session
        session['token'] = token
        print(session['token'])
        return jsonify({'username': username}), 200
        
    return jsonify({'error': 'Invalid username or password'}), 401


# 2. logout route
@api_bp.route('/api/logout', methods=['POST'])
def logout():
    session.pop('token', None)
    return jsonify({'message': 'Successfully logout'}), 200


# 3. record route
@api_bp.route('/api/record', methods=['POST'])   
def record():
    if not check_auth():
        return unauthorized()
        
    data = request.json
    room = data.get('room')
    unique_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO records (id, room) VALUES (?, ?)", (unique_id, room))
    conn.commit()
    
    return jsonify({'unique_id': unique_id}), 200
    

# 4. admin/device route
@api_bp.route('/api/admin/device', methods=['PUT'])
def device(): 
    if not check_auth():
        return unauthorized()
        
    data = request.json
    room = data.get('room')
    public_key = data.get('public_key')
    
    cursor = conn.cursor()
    cursor.execute('REPLACE INTO devices (room, public_key) VALUES (?, ?)', (room, public_key))
    conn.commit()
    
    return jsonify({'room': room}), 200


def get_all_devices():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices")
    rows = cursor.fetchall()
    devices = []
    for row in rows:
        device = {
            'id': row[0],
            'room': row[1],
            'public_key': row[2]
        }
        devices.append(device)

    return devices


# 5. admin/devices route
@api_bp.route('/api/admin/devices', methods=['GET'])
def devices():
    if not check_auth():
        return unauthorized()
    devices = get_all_devices()    
    return jsonify(devices), 200


def get_device_status(room_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices WHERE room_id=?", (room_id,))
    row = cursor.fetchone()
    if row:
        device_status = {
            # Just a demo structure
            'room': row[1],
            'temperature': row[2],
            'wind_speed': row[3],
            'mode': row[4],
            'sweep': bool(row[5]),
            'is_on': bool(row[6]),
            'last_update': row[7]
        }
    else:
        device_status = {}

    return device_status


# 6. status/{room_id} route
@api_bp.route('/api/status/<room_id>', methods=['GET'])
def status_roomid(room_id):
    if not check_auth():
        return unauthorized()
    device_status = get_device_status(room_id)
    return jsonify(device_status), 200


def get_all_device_status():
    cursor = conn.cursor()
    cursor.execute("SELECT room_id, is_on FROM devices")
    rows = cursor.fetchall()
    device_status_list = []
    for row in rows:
        device_status = {
            'room': row[0],
            'is_on': bool(row[1])
        }
        device_status_list.append(device_status)

    return device_status_list


# 7. status route
@api_bp.route('/api/status', methods=['GET'])
def status():
    if not check_auth():
        return unauthorized()
        
    all_device_status = get_all_device_status()
    return jsonify(all_device_status), 200


def save_check_in_time(room, check_in_time):
    cursor = conn.cursor()
    current_time = datetime.datetime.now()
    cursor.execute("INSERT INTO check_ins (room, check_in_time, timestamp) VALUES (?, ?, ?)",
                   (room, check_in_time, current_time))
    conn.commit()
    cursor.close()


# 8. room/check_in route
@api_bp.route('/api/room/check_in', methods=['POST'])
def check_in():
    if not check_auth():
        return unauthorized()
        
    data = request.json
    room = data.get('room')
    check_in_time = data.get('check_in_time')
    save_check_in_time(room, check_in_time)

    return jsonify({'room': room}), 200


def save_check_out_time(room, check_out_time):
    cursor = conn.cursor()
    current_time = datetime.datetime.now()
    cursor.execute("UPDATE check_ins SET check_out_time = ?, timestamp = ? WHERE room = ?",
                   (check_out_time, current_time, room))
    conn.commit()
    cursor.close()

def generate_report(room, check_out_time):
    report_data = {
        'room': room,
        'check_out_time': check_out_time,
        'report_id': str(uuid.uuid4())
        # etc.
    }

    return report_data


# 9. room/check_out route
@api_bp.route('/api/room/check_out', methods=['POST'])
def check_out():
    if not check_auth():
        return unauthorized()
    
    data = request.json
    room = data.get('room')
    check_out_time = data.get('check_out_time')
    save_check_out_time(room, check_out_time)
    report_data = generate_report(room, check_out_time)

    return jsonify({'room': room, 'report': report_data}), 200


def validate_date_format(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def calculate_total_cost(start_date, end_date):
    # Assume that data is stored in a table named `expenses` with `date` and `amount` fields
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?", (start_date, end_date))
    total_cost = cursor.fetchone()[0]
    if total_cost is None:
        total_cost = 0
    cursor.close()

    return total_cost


def calculate_total_income(start_date, end_date):
    # Assume that data is stored in a table named `income` with `date` and `amount` fields
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM income WHERE date BETWEEN ? AND ?", (start_date, end_date))
    total_income = cursor.fetchone()[0]
    if total_income is None:
        total_income = 0
    cursor.close()

    return total_income


# 10. statistics
@api_bp.route('/api/statistics', methods=['GET'])
def statistics():
    if not check_auth():
        return unauthorized()

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Validate start_date and end_date
    if not validate_date_format(start_date) or not validate_date_format(end_date):
        return jsonify({'error': 'Invalid date format'}), 400

    # Perform statistics calculation based on start_date and end_date
    total_cost = calculate_total_cost(start_date, end_date)
    total_income = calculate_total_income(start_date, end_date)

    return jsonify({
        'total_cost': total_cost,
        'total_income': total_income
    }), 200