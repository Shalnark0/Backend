from flask import request, jsonify
from functools import wraps
from app.utils.error_handler import Error


def check_role(required_role: str, user_role: str) -> bool:
    """Проверяет, соответствует ли роль пользователя требуемой."""
    return user_role == required_role

def role_required(required_role):
    """Декоратор для ограничения доступа по ролям."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            user_data = getattr(request, "user", None)
            if not user_data or "role" not in user_data:
                return Error("User data is missing", 403).to_response()

            user_role = user_data["role"]
            if not check_role(required_role, user_role):
                return Error("Access denied: Insufficient role", 403).to_response()

            return func(*args, **kwargs)
        return wrapper
    return decorator



