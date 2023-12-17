from flask import Blueprint, jsonify
from flask_cors import CORS

hello_blueprint = Blueprint("hello", __name__)
CORS(hello_blueprint)

@hello_blueprint.route("/hello", methods=["GET"])
def hello_world():
    return jsonify(message="Hello, World!")
