from flask import Flask, jsonify, request
from flask import Blueprint
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    username = datos.get("username")
    password = datos.get("password")
    if username == "servicesApego" and password == "PMS2025":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401