from flask import Blueprint, request, jsonify, session, Flask
import uuid
import jwt
import sqlite3
import threading

# create blueprint to organize and manage routes and view functions
api_bp = Blueprint('views', __name__)

# connect to SQLite database
conn = sqlite3.connect('buptse.db')
cursor = conn.cursor()

# create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS records
                  (id TEXT PRIMARY KEY, room TEXT)''')

# create a thread-local storage object
local_storage = threading.local()

"""
def get_db_connection():
    if not hasattr(local_storage, 'connection'):
        local_storage.connection = sqlite3.connect('your_database.db')
    return local_storage.connection


def cleanup_db_connection(exception=None):
    if hasattr(local_storage, 'connection'):
        local_storage.connection.close()
"""

# 1. login route
@api_bp.route('/api/login', methods=['POST'])
def login():
    # parse request body to get username and password
    username = request.json.get('username')
    password = request.json.get('password')
    
    # check username and password
    if username == 'admin' and password == 'admin':
        
    #     # [Warning!!!] generate JWT token
    #     token = jwt.encode({'username': username}, app.secret_key)
    #     # save token to session
    #     session['token'] = token
        
        return jsonify({'username': username}), 200
        
    return jsonify({'error': 'Invalid username or password'}), 401

# 2. logout route
@api_bp.route('/api/logout', methods=['POST'])
def logout():
    # [Error] remove token from session
    # session.pop('token', None)
    return jsonify({'message': 'Successfully logout'}), 200


# JWT check logic
def check_auth():
    # get token from session
    token = session.get('token')
    
    # if token is None, return False
    if token is None:
        return False
        
    try:
        # decode token by secret key
        jwt.decode(token, api_bp.secret_key)
        
        # return True if decode successfully
        return True
    except:
        # return False if decode unsuccessfully
        return False

# 401 error handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

# 3. record route
@api_bp.route('/api/record', methods=['POST'])   
def record():
    # check if request is authenticated
    if not check_auth():
        # [Warning!!!] This is where 401 is returned because the token logic hasn't been written yet
        return unauthorized()
        
    # parse request body to get room id
    data = request.json
    
    # get room id from data
    # room = data[0].get('room')
    room = data.get('room')


    """
    |   id (TEXT)   |   room (TEXT)   |
    ----------------------------------
    |   unique_id   |   room_value    |
    """
    
    # save data to SQLite database
    unique_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO records (id, room) VALUES (?, ?)", (unique_id, room))
    conn.commit()

    # close database connection
    conn.close()
    
    return jsonify({'unique_id': unique_id}), 200
    
"""
# The function that closes the database connection is called at the end of each request
@app.teardown_request
def teardown_request(exception=None):
    cleanup_db_connection(exception)
"""

# # 4. admin/device route
# @api_bp.route('/admin/device', methods=['POST'])
# def device(): 
#     # check authorization
#     if not check_auth():
#         return unauthorized()
        
#     # parse request body to get device info
#     data = request.json
    
#     # get room id from data
#     room = data.get('room')
    
#     # get device id from data
#     device_id = data.get('device_id')
    
#     # get device info from data
#     device_info = data.get('device_info')
    
#     # save device info to database
    
#     return jsonify({'unique_id': str(uuid.uuid4())}), 200


# # 5. admin/devices route
# @api_bp.route('/admin/devices', methods=['GET'])
# def devices():
#     # check authorization
#     if not check_auth():
#         return unauthorized()
        
#     # get all devices from database
    
#     return jsonify(devices), 200


# # 6. status/{room_id} route
# @api_bp.route('/status/<room_id>', methods=['GET'])
# def status_roomid(room_id):
#     # check authorization
#     if not check_auth():
#         return unauthorized()
        
#     # return device status for the given room id
#     return jsonify(devices.get(room_id, {})), 200


# # 7. status route
# @api_bp.route('/status', methods=['GET'])
# def status(room_id):
#     # check authorization
#     if not check_auth():
#         return unauthorized()
        
#     # return device status for the given room id
#     return jsonify(devices.get(room_id, {})), 200

# # 8. room/check_in route
# @api_bp.route('/room/check_in', methods=['POST'])
# def check_in():
#     # check authorization
#     if not check_auth():
#         return unauthorized()
        
#     # parse request body to get room id
#     data = request.json

#     # get room id from data
#     room = data.get('room')
    
#     # get check in time from data
#     check_in_time = data.get('check_in_time')
    
#     # save check in time to database
    
#     return jsonify({'unique_id': str(uuid.uuid4())}), 200

# # 9. room/check_out route
# @api_bp.route('/room/check_out', methods=['POST'])
# def check_out():
#     # check authorization
#     if not check_auth():
#         return unauthorized()
        
#     # parse request body to get room id
#     data = request.json
    
#     # get room id from data
#     room = data.get('room')
    
#     # get check out time from data
#     check_out_time = data.get('check_out_time')
    
#     # save check out time to database
    
#     return jsonify({'unique_id': str(uuid.uuid4())}), 200


# # 10. register blueprint to flask app, they will be associated
# app.register_blueprint(api_bp, url_prefix='/api')

# print("Name of Blueprint: ", api_bp.name)
# print("Name of Flask App: ", app.name)

# if __name__ == '__main__':
#     app.run(debug=True, port=11451)