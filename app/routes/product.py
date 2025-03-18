from flask import Blueprint
from app.controllers.product_controller import ProductController

product_routes = Blueprint("product", __name__, url_prefix='/products')

product_routes.route("/add_product", methods=["POST"])(ProductController.add_product)
product_routes.route("/get_products", methods=["GET"])(ProductController.get_all_products)
product_routes.route("/get_product/<string:product_id>", methods=["GET"])(ProductController.get_product_by_id)
product_routes.route("/update_product/<string:product_id>", methods=["PUT"])(ProductController.update_product)
product_routes.route("/delete_product/<string:product_id>", methods=["DELETE"])(ProductController.delete_product)

product_routes.route("/add_to_favorites", methods=["POST"])(ProductController.add_to_favorites)
product_routes.route("/get_favorites", methods=["GET"])(ProductController.get_favorite_products)

