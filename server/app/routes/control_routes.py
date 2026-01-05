from flask import Blueprint, request, jsonify, current_app
from app.services.key_service import (
    generate_signature_keys,
    generate_rsa_keys
)
from app.utils.network_utils import get_local_ip, broadcast_receiver, listen_for_receiver
import threading
from app.extensions import app_state

control_bp = Blueprint("control", __name__)

@control_bp.route("/role/select", methods=["POST"])
def select_role():
    role = request.json.get("role").lower()
    print(f"Role selected: {role}")
    if role not in ["sender", "receiver"]:
        return jsonify({"error": "Invalid role"}), 400

    app_state.role = role.upper()

    # Generate keys on demand
    if role == "sender":
        generate_signature_keys()
        print("Generated signature keys for sender")
    elif role == "receiver":
        generate_rsa_keys()
        print("Generated RSA keys for receiver")

    return jsonify({
        "message": f"Role set to {role}"
    })
    
