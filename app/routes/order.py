from flask import Blueprint
from app.controllers.order_controller import OrderController

order_routes = Blueprint("order", __name__)

order_routes.route("/create_order", methods=["POST"])(OrderController.create_order)
