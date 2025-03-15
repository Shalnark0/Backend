from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product
from app.models.order import Order
from app.models.order import OrderItem
from app.utils.error_handler import BadRequestError, NotFoundError
from uuid import UUID

order_bp = Blueprint('order_bp', __name__)

class OrderService:
    @staticmethod
    def create_order(data, user_id):
        # Проверка, что user_id это байты (16 байтов)
        if isinstance(user_id, str):  # Если user_id — строка UUID
            user_id_bytes = UUID(user_id).bytes  # Преобразуем в байты
        elif isinstance(user_id, bytes):  # Если это уже байты, используем их напрямую
            user_id_bytes = user_id
        else:
            raise BadRequestError("Invalid user ID format. Expected string or bytes.")

        product_name = data.get('product_name')
        quantity = data.get('quantity')
        address = data.get('address')

        if not product_name or not quantity or not address:
            raise BadRequestError("Product name, quantity, and address are required")

        product = Product.query.filter_by(name=product_name).first()
        if not product:
            raise NotFoundError(f"Product '{product_name}' not found")

        if product.amount < quantity:
            raise BadRequestError(f"Not enough stock for product '{product_name}'")

        # Сохраняем user_id как байты
        new_order = Order(user_id=user_id_bytes, address=address, status='pending')
        db.session.add(new_order)
        db.session.flush()

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=quantity,
            price=product.price
        )
        db.session.add(order_item)

        product.amount -= quantity

        db.session.commit()

        return new_order.id


