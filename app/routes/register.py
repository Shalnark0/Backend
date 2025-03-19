from flask import Blueprint
from app.controllers.register_controller import RegisterController

register_routes = Blueprint("register", __name__, url_prefix="/user")

register_routes.route("/register", methods=["POST"])(RegisterController.register)
register_routes.route("/upload_avatar/<string:user_id>", methods=["POST"])(RegisterController.upload_avatar)
