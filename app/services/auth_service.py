import jwt
import datetime
import secrets
import hashlib
from flask import current_app, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, mail
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.utils.error_handler import UnauthorizedError, BadRequestError
from flask_mail import Message

class AuthService:
    @staticmethod
    def login(name, password):
        """Аутентификация пользователя и генерация токенов"""
        user = User.query.filter_by(name=name).first()

        if not user:
            raise UnauthorizedError("Invalid credentials").to_response()

        if not AuthService.verify_password(user.password, password):
            raise UnauthorizedError("Invalid credentials").to_response()

        response = AuthService.generate_tokens(user)

        return response

    @staticmethod
    def get_current_user():
        access_token = AuthService.get_access_token()
        if not access_token:
            raise UnauthorizedError("Access token is missing")

        payload = AuthService.verify_token(access_token)
        print(f"Payload: {payload}")

        user_id = payload.get("id")
        if not user_id:
            raise UnauthorizedError("Invalid token: user ID not found")

        print(f"User ID (string): {user_id}")
        return user_id

    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширует пароль"""
        if not password:
            raise BadRequestError("Password cannot be empty").to_response()
        return generate_password_hash(password)

    @staticmethod
    def verify_password(stored_hash: str, password: str) -> bool:
        """Проверяет пароль"""
        if not stored_hash or not password:
            raise BadRequestError("Both hash and password must be provided").to_response()
        return check_password_hash(stored_hash, password)

    @staticmethod
    def generate_tokens(user):
        """Создаёт Access и Refresh токены и сохраняет их в cookies и БД"""
        access_payload = {
            "id": user.id,
            "role": user.role,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }

        refresh_payload = {
            "id": user.id,
            "role": user.role,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }

        try:
            access_token = jwt.encode(access_payload, current_app.config["SECRET_KEY"], algorithm="HS256")
            refresh_token = jwt.encode(refresh_payload, current_app.config["SECRET_KEY"], algorithm="HS256")
        except Exception as e:
            raise BadRequestError(f"Error generating tokens: {str(e)}").to_response()

        new_refresh_token = RefreshToken(user_id=user.id, token=refresh_token, expires_at=refresh_payload["exp"])
        db.session.add(new_refresh_token)
        db.session.commit()

        response = jsonify({"message": "Tokens generated successfully"})
        response.set_cookie("access_token", access_token, httponly=True, samesite='Strict', max_age=30 * 60)
        response.set_cookie("refresh_token", refresh_token, httponly=True, samesite='Strict', max_age=7 * 24 * 60 * 60)

        return response

    @staticmethod
    def get_tokens_from_cookies():
        """Извлекает Access и Refresh токены из cookies"""
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if not access_token or not refresh_token:
            raise UnauthorizedError("Missing tokens in cookies").to_response()

        return access_token, refresh_token

    @staticmethod
    def get_access_token():
        """Извлекает Access токен из заголовка Authorization или из cookies"""
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return request.cookies.get("access_token")

    @staticmethod
    def verify_token(token):
        """Проверяет валидность токена"""
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token has expired").to_response()
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Invalid token").to_response()

    @staticmethod
    def refresh_token():
        """Обновляет Access токен на основе Refresh токена из БД"""
        try:
            _, refresh_token = AuthService.get_tokens_from_cookies()
            payload = AuthService.verify_token(refresh_token)

            db_token = RefreshToken.query.filter_by(token=refresh_token).first()
            if not db_token:
                raise UnauthorizedError("Refresh token not found in database")

            if db_token.expires_at < datetime.datetime.utcnow():
                db.session.delete(db_token)
                db.session.commit()
                raise UnauthorizedError("Refresh token expired")

            new_access_token = jwt.encode(
                {
                    "id": payload["id"],
                    "role": payload.get("role"),
                    "iat": datetime.datetime.utcnow(),
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                },
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            )

        except Exception as e:
            raise UnauthorizedError(f"Failed to refresh token: {str(e)}")

        response = jsonify({"message": "Access token refreshed"})
        response.set_cookie("access_token", new_access_token, httponly=True, secure=True, samesite='Strict',
                            max_age=30 * 60)
        return response

    @staticmethod
    def logout():
        """Удаляет Refresh-токен из БД, куков и деактивирует пользователя"""
        try:
            _, refresh_token = AuthService.get_tokens_from_cookies()

            db_token = RefreshToken.query.filter_by(token=refresh_token).first()
            if db_token:
                db.session.delete(db_token)
                db.session.commit()

            payload = AuthService.verify_token(refresh_token)
            user_id = payload.get("id")
            if not user_id:
                raise UnauthorizedError("User ID not found in token").to_response()

            user = User.query.get(user_id)
            if user:
                user.is_active = 0
                db.session.commit()

            response = jsonify({"message": "Logged out successfully"})
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

            return response

        except Exception as e:
            raise UnauthorizedError(f"Failed to logout: {str(e)}")

    @staticmethod
    def generate_reset_token(email):
        """Генерация токена на основе email."""
        random_bytes = secrets.token_bytes(32)
        token = hashlib.sha256(f"{email}{random_bytes}".encode()).hexdigest()
        return token

    @staticmethod
    def send_reset_password_email(email):
        """Отправка письма для сброса пароля."""
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("User not found")

        reset_token = AuthService.generate_reset_token(email)
        reset_link = f"http://example.com/reset-password?token={reset_token}"

        msg = Message("Password Reset Request", recipients=[email])
        msg.body = f"Click the link to reset your password: {reset_link}"

        mail.send(msg)

