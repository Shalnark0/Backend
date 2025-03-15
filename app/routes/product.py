from flask import Blueprint
from app.controllers.product_controller import ProductController

product_routes = Blueprint("product", __name__)

product_routes.route("/add_product", methods=["POST"])(ProductController.add_product)
product_routes.route("/update_product/<int:product_id>", methods=["PUT"])(ProductController.update_product)
product_routes.route("/add_to_favorites", methods=["POST"])(ProductController.add_to_favorites)
