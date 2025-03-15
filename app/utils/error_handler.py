from flask import jsonify

class Error(Exception):
    """Базовый класс для всех пользовательских ошибок"""
    def __init__(self, message="Internal server error", status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_response(self):
        return jsonify({"error": self.message}), self.status_code


class NotFoundError(Error):
    """Ошибка 404: Ресурс не найден"""
    def __init__(self, message="Not Found"):
        super().__init__(message, 404)


class BadRequestError(Error):
    """Ошибка 400: Некорректный запрос"""
    def __init__(self, message="Bad Request"):
        super().__init__(message, 400)


class UnauthorizedError(Error):
    """Ошибка 401: Доступ запрещен"""
    def __init__(self, message="You don't have access rights"):
        super().__init__(message, 401)


class ConflictError(Error):
    """Ошибка 409: Конфликт"""
    def __init__(self, message="Conflict"):
        super().__init__(message, 409)


class InternalServerError(Error):
    """Ошибка 500: Внутренняя ошибка сервера"""
    def __init__(self, message="Internal Server Error"):
        super().__init__(message, 500)
