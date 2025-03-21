from flask import Blueprint
from app.controllers.user_controller import UserController

user_routes = Blueprint("user", __name__)

user_routes.route("/user", methods=["POST"])(UserController.register)
user_routes.route("/user", methods=["GET"])(UserController.get_users)
user_routes.route("/user/<string:user_id>", methods=["GET"])(UserController.get_user_by_id)
user_routes.route("/user/<string:user_id>", methods=["PUT"])(UserController.redact_user)
user_routes.route("/user/<string:user_id>", methods=["DELETE"])(UserController.delete_user)