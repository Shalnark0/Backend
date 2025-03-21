from flask import jsonify, request
from app.services.auth_service import AuthService
from app.utils.error_handler import Error


class AuthController:
    @staticmethod
    def login():
        data = request.get_json()
        name = data.get("name")
        password = data.get("password")

        if not name or not password:
            return Error("Name and password are required", 400).to_response()

        response = AuthService.login(name, password)

        return response

    @staticmethod
    def refresh():
        try:
            response = AuthService.refresh_token()
            return response
        except Exception as e:
            return Error(str(e), 401).to_response()

    @staticmethod
    def logout():
        return AuthService.logout()

    @staticmethod
    def reset_pass():
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({"error": "Email is required"}), 400
        try:
            AuthService.send_reset_password_email(email)
            return jsonify({"message": "Password reset email sent"}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "Failed to send email"}), 500