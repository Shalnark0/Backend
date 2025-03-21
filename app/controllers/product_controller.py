from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService
from app.services.auth_service import AuthService
from app.services.favorite_service import FavoriteService
from app.utils.error_handler import BadRequestError, NotFoundError
import uuid

class ProductController:
    @staticmethod
    def add_product():
        data = request.form
        photos = request.files.getlist("photos")
        try:
            product_id = ProductService.add_product(data, photos)
            return jsonify({"message": "Product created successfully"}), 201
        except BadRequestError as e:
            return jsonify({"message": str(e)}), 400

    @staticmethod
    def update_product(product_id):
        data = request.get_json()
        try:
            ProductService.update_product(product_id, data)
            return jsonify({"message": "Product updated successfully"})
        except NotFoundError as e:
            return jsonify({"message": str(e)}), 404
        except BadRequestError as e:
            return jsonify({"message": str(e)}), 400

    @staticmethod
    def delete_product(product_id):
        try:
            ProductService.delete_product(product_id)
            return jsonify({"message": "Product deleted successfully"})
        except NotFoundError as e:
            return jsonify({"message": str(e)}), 404
        except BadRequestError as e:
            return jsonify({"message": str(e)}), 400

    @staticmethod
    def get_all_products():
        products = ProductService.get_all_products()
        return jsonify(products), 200

    @staticmethod
    def get_product_by_id(product_id):
        try:
            product = ProductService.get_product_by_id(product_id)
            return jsonify(product), 200
        except NotFoundError as e:
            return jsonify({"message": str(e)}), 404

    @staticmethod
    def get_favorite_products():
        user_id = AuthService.get_current_user()
        favorite_products = FavoriteService.get_favorite_products(user_id)
        return jsonify(favorite_products), 200

    @staticmethod
    def add_to_favorites():
        data = request.get_json()
        product_id_str = data.get("product_id")
        user_id = AuthService.get_current_user()

        if product_id_str:
            if product_id_str.startswith("0x"):
                product_id_str = product_id_str[2:]

            try:
                product_id_str = str(uuid.UUID(product_id_str))
            except ValueError:
                return jsonify({"message": "Invalid UUID format for product_id"}), 400
        else:
            return jsonify({"message": "Product ID is required"}), 400

        try:
            FavoriteService.add_to_favorites(user_id, product_id_str)
            return jsonify({"message": "Product added to favorites successfully"}), 201
        except Exception as e:
            return jsonify({"message": f"Error adding product to favorites: {str(e)}"}), 400

    @staticmethod
    def delete_favorite(product_id):
        user_id = AuthService.get_current_user()

        try:
            FavoriteService.delete_favorite(user_id, product_id)
            return jsonify({"message": "Product removed from favorites successfully"}), 200
        except NotFoundError as e:
            return jsonify({"message": str(e)}), 404
        except BadRequestError as e:
            return jsonify({"message": str(e)}), 400

