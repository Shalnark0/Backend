from app import db
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.error_handler import ConflictError, BadRequestError, NotFoundError
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')

class RegisterService:
    @staticmethod
    def register_user(data):
        """Регистрирует нового пользователя с поддержкой аватара (base64 строка)"""
        name = data.get("name")
        password = data.get("password")
        email = data.get("email")
        avatar = data.get("avatar")

        if not name or not password or not email:
            raise BadRequestError("All fields are required")

        existing_user = User.query.filter_by(name=name).first()
        if existing_user:
            raise ConflictError(f"User with name '{name}' already exists")
        if avatar:
            if not isinstance(avatar, str) or not avatar.startswith("data:image/"):
                raise BadRequestError("Avatar must be a valid base64 image string")

        new_user = User(
            name=name,
            password=AuthService.hash_password(password),
            email=email,
            role=data.get("role", "user"),
            avatar=avatar
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201

    @staticmethod
    def upload_avatar(user_id, avatar):
        if avatar.filename == '':
            raise BadRequestError("No selected file")

        file_ext = os.path.splitext(avatar.filename)[1].lower()
        if file_ext not in (".jpeg", ".png", ".jpg"):
            raise BadRequestError("Only JPEG and PNG images are allowed")

        filename = secure_filename(f"{user_id}{file_ext}")

        avatar_path = os.path.join('uploads', filename)

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        avatar.save(os.path.join(UPLOAD_FOLDER, filename))

        user = User.query.get(user_id)
        if not user:
            raise NotFoundError("User not found")

        user.avatar = avatar_path
        db.session.commit()

        return {"message": "Avatar uploaded successfully", "avatar_path": avatar_path}

