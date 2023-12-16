import os
import base64
from flask import Blueprint, request, jsonify, session
from flask_cors import CORS

auth_blueprint = Blueprint("auth", __name__)
CORS(auth_blueprint)

def generate_csrf_token():
    return base64.b64encode(os.urandom(32)).decode('utf-8')

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request data"}), 400

    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin":
        session["user_id"] = 1
        session.permanent = True
        csrf_token = generate_csrf_token()
        session["csrf_token"] = csrf_token
        return jsonify({"username": username, "csrf_token": csrf_token}), 200
    else:
        return jsonify({"error": "Login failed"}), 401

@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    if "session" in request.cookies:
        response = jsonify({"message": "Logout successfully"})
        response.delete_cookie("session")
        return response, 200
    else:
        return jsonify({"message": "Not logged in"}), 401


# import os
# import base64
# from flask import Blueprint, request, jsonify, session, current_app
# from app import db
# from werkzeug.security import check_password_hash
# from app.models import User
# from flask_cors import CORS

# auth_blueprint = Blueprint("auth", __name__)
# CORS(auth_blueprint)

# def generate_csrf_token():
#     return base64.b64encode(os.urandom(32)).decode('utf-8')

# # @admin_blueprint.route("/login", methods=["POST"])
# @auth_blueprint.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Invalid request data"}), 400

#     username = data.get("username")
#     password = data.get("password")

#     user = User.query.filter_by(username=username).first()

#     if user and check_password_hash(user.password_hash, password):
#         session["user_id"] = user.id
#         session.permanent = True
#         csrf_token = generate_csrf_token()
#         session["csrf_token"] = csrf_token
#         return jsonify({"username": user.username, "csrf_token": csrf_token}), 200
#     else:
#         return jsonify({"error": "Login failed"}), 401

# # @admin_blueprint.route("/logout", methods=["POST"])
# @auth_blueprint.route("/logout", methods=["POST"])
# def logout():
#     if "session" in request.cookies:
#         response = jsonify({"message": "Logout successfully"})
#         response.delete_cookie("session")
#         return response, 204
#     else:
#         return jsonify({"message": "Not logged in"}), 401