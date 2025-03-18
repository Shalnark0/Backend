from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.services.order_service import OrderService
from app.utils.error_handler import BadRequestError, NotFoundError

order_bp = Blueprint('order_bp', __name__)

class OrderController:
    @staticmethod
    def create_order():
        user_id = AuthService.get_current_user()
        print(f"User ID in Controller (bytes): {user_id}")
        data = request.get_json()
        try:
            order_id = OrderService.create_order(data, user_id)
            return jsonify({"message": "Order created successfully", "order_id": str(order_id)}), 201
        except (BadRequestError, NotFoundError) as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def update_order(order_id):
        user_id = AuthService.get_current_user()
        print(f"User ID in Controller (bytes): {user_id}")
        data = request.get_json()
        try:
            updated_order = OrderService.update_order(order_id, data, user_id)
            return jsonify({"message": "Order updated successfully", "order_id": str(updated_order.id)}), 200
        except (BadRequestError, NotFoundError) as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete_order(order_id):
        user_id = AuthService.get_current_user()
        print(f"User ID in Controller (bytes): {user_id}")
        try:
            OrderService.delete_order(order_id, user_id)
            return jsonify({"message": "Order deleted successfully"}), 200
        except (BadRequestError, NotFoundError) as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_orders():
        user_id = AuthService.get_current_user()
        print(f"User ID in Controller (bytes): {user_id}")
        try:
            orders = OrderService.get_orders(user_id)
            return jsonify({"orders": orders}), 200
        except NotFoundError as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def get_order_by_id(order_id):
        user_id = AuthService.get_current_user()
        print(f"User ID in Controller (bytes): {user_id}")
        try:
            order = OrderService.get_order_by_id(order_id, user_id)
            return jsonify({"order": order}), 200
        except (NotFoundError, BadRequestError) as e:
            return jsonify({"error": str(e)}), 404
