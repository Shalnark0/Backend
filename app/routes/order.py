from flask import Blueprint
from app.controllers.order_controller import OrderController

order_routes = Blueprint("order", __name__, url_prefix='/orders')

order_routes.route("/order", methods=["POST"])(OrderController.create_order)
order_routes.route("/order/<string:order_id>", methods=["PUT"])(OrderController.update_order)
order_routes.route("/order/<string:order_id>", methods=["DELETE"])(OrderController.delete_order)
order_routes.route("/order", methods=["GET"])(OrderController.get_orders)
order_routes.route("/order/<string:order_id>", methods=["GET"])(OrderController.get_order_by_id)
