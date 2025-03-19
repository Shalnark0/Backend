from flask import request, jsonify, send_from_directory, abort
import os, logging
from app.models.user import User
from app.services.register_service import RegisterService
from app.utils.error_handler import Error, ConflictError, BadRequestError, NotFoundError

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))

class RegisterController:
    @staticmethod
    def register():
        data = request.get_json()

        name = data.get("name")
        password = data.get("password")
        email = data.get("email")
        avatar = data.get("avatar")

        if not name or not password or not email:
            return Error("Name, password, and email are required", 400).to_response()

        try:
            RegisterService.register_user({
                "name": name,
                "password": password,
                "email": email,
                "avatar": avatar
            })
        except (ConflictError, BadRequestError) as e:
            return Error(str(e), 400).to_response()

        return jsonify({"message": "User registered successfully"}), 201

    @staticmethod
    def upload_avatar(user_id):
        if 'avatar' not in request.files:
            return Error("Avatar is required", 400).to_response()

        avatar = request.files['avatar']

        try:
            result = RegisterService.upload_avatar(user_id, avatar)
        except (NotFoundError, BadRequestError) as e:
            return Error(str(e), 400).to_response()

        return jsonify(result), 200

    @staticmethod
    def get_avatar(user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return Error("User not found", 404).to_response()

            avatar_path = user.avatar
            if not avatar_path:
                return Error("Avatar not found", 404).to_response()

            filename = os.path.basename(avatar_path)

            full_path = os.path.join(UPLOAD_FOLDER, filename)

            if not os.path.exists(full_path):
                return Error("Avatar file does not exist", 404).to_response()

            return send_from_directory(UPLOAD_FOLDER, filename), 200

        except Exception as e:
            logging.error(f"Error retrieving avatar for user {user_id}: {str(e)}")
            return Error("Error retrieving avatar", 500).to_response()



