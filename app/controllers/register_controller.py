from flask import request, jsonify
from app.services.register_service import RegisterService
from app.utils.error_handler import Error, ConflictError, BadRequestError

class RegisterController:
    @staticmethod
    def register():
        # Получаем данные как JSON
        data = request.get_json()

        # Извлекаем необходимые данные из JSON
        name = data.get("name")
        password = data.get("password")
        email = data.get("email")
        avatar = data.get("avatar")  # Если avatar нужно передавать как файл, это потребует дополнительной обработки

        if not name or not password or not email:
            return Error("Name, password, and email are required", 400).to_response()

        try:
            RegisterService.register_user({
                "name": name,
                "password": password,
                "email": email,
                "avatar": avatar  # avatar в JSON может быть представлено как строка или base64
            })
        except (ConflictError, BadRequestError) as e:
            return Error(str(e), 400).to_response()

        return jsonify({"message": "User registered successfully"}), 201

