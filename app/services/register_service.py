from app import db
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.error_handler import ConflictError, BadRequestError


class RegisterService:
    @staticmethod
    def register_user(data):
        """Регистрирует нового пользователя"""

        if not data.get("name") or not data.get("password") or not data.get("email"):
            raise BadRequestError("All fields are required")

        existing_user = User.query.filter_by(name=data["name"]).first()
        if existing_user:
            raise ConflictError(f"User with name '{data['name']}' already exists")

        # Создание нового пользователя
        new_user = User(
            name=data["name"],
            password=AuthService.hash_password(data["password"]),
            email=data["email"],
            role=data.get("role", "user")
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201
