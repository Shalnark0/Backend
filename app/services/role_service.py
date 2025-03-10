from flask import request, jsonify
from functools import wraps
from app.models.article import Article
from app import db
from app.utils.error_handler import ErrorHandler


def check_role(required_role: str, user_role: str) -> bool:
    """Проверяет, соответствует ли роль пользователя требуемой."""
    return user_role == required_role

def role_required(required_role):
    """Декоратор для ограничения доступа по ролям."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем данные пользователя из запроса
            user_data = getattr(request, "user", None)
            if not user_data or "role" not in user_data:
                return ErrorHandler("User data is missing", 403).to_response()

            user_role = user_data["role"]
            if not check_role(required_role, user_role):
                return ErrorHandler("Access denied: Insufficient role", 403).to_response()

            return func(*args, **kwargs)
        return wrapper
    return decorator



def is_author_required(func):
    """Декоратор для проверки, является ли пользователь автором статьи."""

    @wraps(func)
    def wrapper(article_id, *args, **kwargs):
        user_data = getattr(request, "user", None)
        if not user_data:
            return ErrorHandler("User data is missing", 400).to_response()  # Ошибка, если нет данных пользователя

        article = db.session.get(Article, article_id)
        if not article:
            return ErrorHandler("Article not found", 404).to_response()  # Ошибка, если статья не найдена

        if article.author_id != user_data["id"]:  # Сравниваем ID автора и текущего пользователя
            return ErrorHandler("Access denied: You are not the author of this article", 403).to_response()  # Ошибка доступа

        return func(article_id, *args, **kwargs)

    return wrapper

