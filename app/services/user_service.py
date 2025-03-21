from app import db
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.error_handler import ConflictError, BadRequestError, NotFoundError
import os, uuid
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')

class UserService:
    @staticmethod
    def register_user(data):
        name = data.get("name")
        password = data.get("password")
        email = data.get("email")

        if not name or not password or not email:
            raise BadRequestError("All fields are required")

        existing_user = User.query.filter_by(name=name).first()
        if existing_user:
            raise ConflictError(f"User with name '{name}' already exists")

        new_user = User(
            name=name,
            password=AuthService.hash_password(password),
            email=email,
            role=data.get("role", "user")
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201

    @staticmethod
    def delete_user(user_id):
        if not user_id:
            raise ValueError("User ID is required")

        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        db.session.delete(user)
        db.session.commit()

        return {"message": f"User with ID {user_id} has been deleted successfully"}

    @staticmethod
    def redact_user(user_id, data, avatar=None):
        user = User.query.get(user_id)

        if not user:
            raise NotFoundError("User not found").to_response()

        user.name = data.get("name", user.name)
        user.password = data.get("password", user.password)
        user.email = data.get("email", user.email)

        if avatar:
            if avatar.filename == '':
                raise BadRequestError("No file selected for avatar")

            if not avatar.filename.strip():
                raise BadRequestError("File has no valid name")

            if not avatar.filename.lower().endswith(('png', 'jpg', 'jpeg')):
                raise BadRequestError("Invalid file format for avatar")

            unique_id = str(uuid.uuid4())[:8]
            new_filename = f"{unique_id}_{secure_filename(avatar.filename)}"

            avatar_path = os.path.join(UPLOAD_FOLDER, new_filename)

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            avatar.save(avatar_path)

            user.avatar = f"{unique_id}_{secure_filename(avatar.filename)}"

        try:
            db.session.commit()
            return {"message": "User updated successfully"}
        except Exception as e:
            db.session.rollback()
            raise BadRequestError(f"Error updating user: {str(e)}").to_response()

    @staticmethod
    def get_user_by_id(user_id):
        user = db.session.get(User, user_id)
        if not user:
            raise NotFoundError("User not found").to_response()

        return {
            "id": user.id,
            "name": user.name,
            "password": user.password,
            "email": user.email,
            "avatar": user.avatar,
            "is_active": user.is_active,
            "role": user.role
        }

    @staticmethod
    def get_all_users():

        users = db.session.query(User).all()

        return [
            {
                "id": user.id,
                "name": user.name,
                "password": user.password,
                "email": user.email,
                "avatar": user.avatar,
                "role": user.role,
                "is_active": user.is_active
            } for user in users
        ]