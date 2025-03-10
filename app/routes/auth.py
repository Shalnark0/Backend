from flask import Blueprint, request, jsonify
from app.models.user import User
from app.services.auth_service import AuthService
from app import db
from app.utils.error_handler import ErrorHandler

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    user = User.query.filter_by(name=name).first()
    if user and AuthService.verify_password(user.password, password):
        access_token, refresh_token = AuthService.generate_tokens(user)
        return jsonify({"message": "Login successful", "access_token": access_token, "refresh_token": refresh_token}), 200

    return ErrorHandler("Invalid credentials", 401).to_response()

@auth_routes.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return ErrorHandler("Refresh token is missing!", 401).to_response()

    payload = AuthService.verify_token(refresh_token)
    if not payload:
        return ErrorHandler("Invalid or expired refresh token!", 401).to_response()

    user = User.query.get(payload["id"])
    if not user:
        return ErrorHandler("User not found!", 404).to_response()

    access_token, _ = AuthService.generate_tokens(user)
    return jsonify({"access_token": access_token}), 200
