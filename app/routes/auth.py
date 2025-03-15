from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_routes = Blueprint("auth", __name__)

auth_routes.route("/login", methods=["POST"])(AuthController.login)
auth_routes.route("/refresh", methods=["POST"])(AuthController.refresh)
auth_routes.route("/logout", methods=["POST"])(AuthController.logout)
