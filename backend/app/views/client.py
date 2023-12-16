from flask import Blueprint, request, jsonify
from flask_cors import CORS

client_blueprint = Blueprint("client", __name__)
CORS(client_blueprint)

# Judge whether the client is online
@client_blueprint.route("/device/client", methods=["POST"])
def handle_client_online():
    data = request.json

    room_id = data.get("room_id")
    port = data.get("port")
    unique_id = data.get("unique_id")
    signature = data.get("signature")

    # Signature verification and other operations
    pass

    return jsonify({"message": "Online successfully"}), 204


# Handle client requests
@client_blueprint.route("/device/client/<room_id>", methods=["POST"])
def handle_client_operation(room_id):
    # Handle requests
    data = request.json

    operation = data.get("operation")
    request_data = data.get("data")

    # Handle client requests
    pass

    return jsonify({"message": "Operation Request successfully"}), 204
