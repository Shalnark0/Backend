from flask import jsonify, request
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.utils.error_handler import Error


class AuthController:
    @staticmethod
    def login():
        """Аутентификация и установка токенов в cookies"""
        data = request.get_json()
        name = data.get("name")
        password = data.get("password")

        if not name or not password:
            return Error("Name and password are required", 400).to_response()

        response = AuthService.login(name, password)

        return response

    @staticmethod
    def refresh():
        """Обновление access токена с использованием refresh токена из cookies"""
        try:
            response = AuthService.refresh_token()
            return response
        except Exception as e:
            return Error(str(e), 401).to_response()

    @staticmethod
    def logout():
        """Выход из системы (удаляет Refresh-токен)"""
        return AuthService.logout()