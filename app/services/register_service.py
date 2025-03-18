from app import db
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.error_handler import ConflictError, BadRequestError


class RegisterService:
    @staticmethod
    def register_user(data):
        """Регистрирует нового пользователя с поддержкой аватара"""
        name = data.get("name")
        password = data.get("password")
        email = data.get("email")
        avatar = data.get("avatar")

        if not name or not password or not email:
            raise BadRequestError("All fields are required")

        existing_user = User.query.filter_by(name=name).first()
        if existing_user:
            raise ConflictError(f"User with name '{name}' already exists")

        avatar_data = avatar.read() if avatar else None

        new_user = User(
            name=name,
            password=AuthService.hash_password(password),
            email=email,
            role=data.get("role", "user"),
            avatar=avatar_data
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201
