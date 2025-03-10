from flask import Blueprint, request, current_app
from app import db
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.error_handler import ErrorHandler

register_routes = Blueprint("register", __name__)


@register_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user = User.query.filter_by(name=data["name"]).first()
    if user:
        return ErrorHandler("User with this name already exists", 400).to_response()

    new_user = User(
        name=data["name"],
        password=AuthService.hash_password(data["password"]),
        email=data["email"],
        role=data["role"]
    )

    with current_app.app_context():
        db.session.add(new_user)
        db.session.commit()

    return {"message": "User registered successfully"}, 201
