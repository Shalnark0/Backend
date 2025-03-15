from flask import Blueprint, request, jsonify
from app import db
from app.models.favorite import Favorite
from app.models.product import Product
from app.models.user import User
from app.services.favorite_service import FavoriteService
from app.services.product_service import ProductService
from app.utils.error_handler import Error
import uuid


class ProductController:
    @staticmethod
    def add_product():
        data = request.get_json()
        product_id = ProductService.add_product(data)

        # Преобразуем UUID (тип bytes) в строку
        product_id_str = product_id.hex()  # hex() преобразует байты в строку в шестнадцатеричном формате

        return jsonify({"message": "Product created successfully", "product_id": product_id_str}), 201

    @staticmethod
    def update_product(product_id):
        data = request.get_json()
        ProductService.update_product(product_id, data)
        return jsonify({"message": "Product updated successfully"})

    @staticmethod
    def add_to_favorites():
        data = request.get_json()
        user_id_str = data.get("user_id")
        product_id_str = data.get("product_id")


        if user_id_str and user_id_str.startswith("0x"):
            user_id_str = user_id_str[2:]
        if product_id_str and product_id_str.startswith("0x"):
            product_id_str = product_id_str[2:]


        try:
            user_id_bytes = uuid.UUID(user_id_str).bytes
            product_id_bytes = uuid.UUID(product_id_str).bytes
        except ValueError:
            return jsonify({"message": "Invalid UUID format"}), 400


        try:
            FavoriteService.add_to_favorites(user_id_bytes, product_id_bytes)
            return jsonify({"message": "Product added to favorites successfully"}), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 400
