from flask import request, jsonify
from app.services.register_service import RegisterService
from app.utils.error_handler import Error, ConflictError, BadRequestError, NotFoundError


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


