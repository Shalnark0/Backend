import jwt
import datetime
from flask import request, jsonify, current_app
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from app.utils.error_handler import ErrorHandler


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        if not password:
            raise ValueError("Password cannot be empty")
        return generate_password_hash(password)

    @staticmethod
    def verify_password(stored_hash: str, password: str) -> bool:
        if not stored_hash or not password:
            raise ValueError("Both hash and password must be provided")
        return check_password_hash(stored_hash, password)

    @staticmethod
    def generate_tokens(user):
        """Создаёт Access и Refresh токены"""
        access_payload = {
            "id": user.id,
            "role": user.role,
            "iat": datetime.datetime.utcnow(),  # Время создания токена
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Access токен на 30 минут
        }

        refresh_payload = {
            "id": user.id,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Refresh токен на 7 дней
        }

        access_token = jwt.encode(access_payload, current_app.config["SECRET_KEY"], algorithm="HS256")
        refresh_token = jwt.encode(refresh_payload, current_app.config["SECRET_KEY"], algorithm="HS256")

        return access_token, refresh_token

    @staticmethod
    def verify_token(token):
        """Проверяет валидность токена"""
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Токен истёк
        except jwt.InvalidTokenError:
            return None  # Некорректный токен


def token_required(f):
    """Декоратор для проверки Access токена"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return ErrorHandler("Token is missing", 401).to_response()  # Ошибка, если токен отсутствует

        try:
            token = token.split(" ")[1]  # Bearer <token>
            payload = AuthService.verify_token(token)
            if not payload:
                return ErrorHandler("Invalid or expired token", 401).to_response()  # Ошибка, если токен невалидный или просрочен
            # Добавляем информацию о пользователе в request
            request.user = payload
        except Exception as e:
            return ErrorHandler("Token error", 401).to_response()  # Ошибка обработки токена

        return f(*args, **kwargs)

    return decorated


