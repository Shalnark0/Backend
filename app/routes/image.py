from flask import Blueprint
from app.controllers.image_controller import ImageController

image_routes = Blueprint("image", __name__)

image_routes.route("/images/<string:image_id>", methods=["GET"])(ImageController.get_image)