from flask import request, jsonify
from app.services.register_service import RegisterService  # Импортируем RegisterService
from app.utils.error_handler import Error, ConflictError


class RegisterController:
    @staticmethod
    def register():
        data = request.get_json()

        if not data.get("name") or not data.get("password") or not data.get("email"):
            return Error("Name, password, and email are required", 400).to_response()

        # Теперь проверка существует ли пользователь будет делаться в сервисе
        try:
            RegisterService.register_user(data)  # Просто вызываем метод из RegisterService
        except ConflictError as e:
            return Error(str(e), 400).to_response()

        return jsonify({"message": "User registered successfully"}), 201
