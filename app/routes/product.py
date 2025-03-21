from flask import Blueprint
from app.controllers.product_controller import ProductController

product_routes = Blueprint("product", __name__)

product_routes.route("/product", methods=["POST"])(ProductController.add_product)
product_routes.route("/product", methods=["GET"])(ProductController.get_all_products)
product_routes.route("/product/<string:product_id>", methods=["GET"])(ProductController.get_product_by_id)
product_routes.route("/product/<string:product_id>", methods=["PUT"])(ProductController.update_product)
product_routes.route("/product/<string:product_id>", methods=["DELETE"])(ProductController.delete_product)


product_routes.route("/favorite", methods=["POST"])(ProductController.add_to_favorites)
product_routes.route("/favorite", methods=["GET"])(ProductController.get_favorite_products)
product_routes.route("/favorite/<string:product_id>", methods=["DELETE"])(ProductController.delete_favorite)

