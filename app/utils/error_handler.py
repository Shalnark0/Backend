from flask import jsonify

class ErrorHandler:
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

    def to_response(self):
        return jsonify({"error": self.message}), self.status_code
