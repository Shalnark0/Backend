from flask import Blueprint
from app.controllers.register_controller import RegisterController

register_routes = Blueprint("register", __name__)

register_routes.route("/register", methods=["POST"])(RegisterController.register)
