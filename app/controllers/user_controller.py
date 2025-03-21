from flask import request, jsonify, send_from_directory, abort
import os, logging
from app.models.user import User
from app.services.user_service import UserService
from app.utils.error_handler import Error, ConflictError, BadRequestError, NotFoundError

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))

class UserController:
    @staticmethod
    def register():
        data = request.get_json()

        name = data.get("name")
        password = data.get("password")
        email = data.get("email")

        if not name or not password or not email:
            return Error("Name, password, and email are required", 400).to_response()

        try:
            UserService.register_user({
                "name": name,
                "password": password,
                "email": email
            })
        except (ConflictError, BadRequestError) as e:
            return Error(str(e), 400).to_response()

        return jsonify({"message": "User registered successfully"}), 201

    @staticmethod
    def redact_user(user_id):
        data = request.form
        avatar = request.files.get("avatar")
        try:
            UserService.redact_user(user_id, data, avatar)
            return jsonify({"message": "User updated successfully"})
        except NotFoundError as e:
            return jsonify({"message": str(e)}), 404
        except BadRequestError as e:
            return jsonify({"message": str(e)}), 400

    @staticmethod
    def delete_user(user_id):
        try:
            response = UserService.delete_user(user_id)
            return jsonify(response), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

    @staticmethod
    def get_users():
        users = UserService.get_all_users()
        return jsonify(users), 200

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = UserService.get_user_by_id(user_id)
            return jsonify(user), 200
        except NotFoundError as e:
            return jsonify({"message": str(e)}), 404