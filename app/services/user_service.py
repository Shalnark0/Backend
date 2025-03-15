from app import db
from app.models.user import User
from app.utils.error_handler import NotFoundError, ConflictError


class UserService:
    @staticmethod
    def get_user_by_name(name: str) -> User:
        """
        Получить пользователя по имени.
        """
        user = User.query.filter_by(name=name).first()
        if not user:
            raise NotFoundError(f"User with name '{name}' not found")
        return user

    @staticmethod
    def create_user(name: str, password: str, email: str, role: str = 'user') -> User:
        """
        Создать нового пользователя.
        """
        if User.query.filter_by(name=name).first():
            raise ConflictError(f"User with name '{name}' already exists")
        if User.query.filter_by(email=email).first():
            raise ConflictError(f"User with email '{email}' already exists")

        new_user = User(name=name, password=password, email=email, role=role)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def delete_user_by_name(name: str):
        """
        Удалить пользователя по имени.
        """
        user = UserService.get_user_by_name(name)
        db.session.delete(user)
        db.session.commit()
