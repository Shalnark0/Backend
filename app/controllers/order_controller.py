from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.services.order_service import OrderService
import uuid
from app.utils.error_handler import BadRequestError

class OrderController:
    @staticmethod
    def create_order():
        user_id = AuthService.get_current_user()
        print(f"User ID in Controller (bytes): {user_id}")
        data = request.get_json()
        order_id = OrderService.create_order(data, user_id)
        print(order_id)
        return jsonify({"message": "Order created successfully", "order_id": str(order_id)}), 201