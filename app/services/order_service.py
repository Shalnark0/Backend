from app import db
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.utils.error_handler import BadRequestError, NotFoundError
from uuid import UUID

class OrderService:
    @staticmethod
    def create_order(data, user_id):

        if isinstance(user_id, str):
            user_id_str = user_id
        else:
            raise BadRequestError("Invalid user ID format. Expected string.")

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

        new_order = Order(user_id=user_id_str, address=address, total_price=quantity * product.price,
                            status='pending')
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

    @staticmethod
    def update_order(order_id, data, user_id):

        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            raise NotFoundError(f"Order with ID '{order_id}' not found for user '{user_id}'")

        product_name = data.get('product_name')
        quantity = data.get('quantity')
        address = data.get('address')

        if product_name:
            product = Product.query.filter_by(name=product_name).first()
            if not product:
                raise NotFoundError(f"Product '{product_name}' not found")

            if product.amount < quantity:
                raise BadRequestError(f"Not enough stock for product '{product_name}'")

            order.total_price = quantity * product.price

            order_item = OrderItem.query.filter_by(order_id=order.id).first()
            if order_item:
                order_item.product_id = product.id
                order_item.quantity = quantity
                order_item.price = product.price

            product.amount -= quantity

        if address:
            order.address = address

        db.session.commit()

        return order

    @staticmethod
    def delete_order(order_id, user_id):

        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            raise NotFoundError(f"Order with ID '{order_id}' not found for user '{user_id}'")

        OrderItem.query.filter_by(order_id=order_id).delete()

        db.session.delete(order)
        db.session.commit()

    @staticmethod
    def get_orders(user_id):

        orders = Order.query.filter_by(user_id=user_id).all()
        if not orders:
            raise NotFoundError(f"No orders found for user '{user_id}'")

        return [
            {
                "id": order.id,
                "address": order.address,
                "total_price": order.total_price,
                "status": order.status,
                "order_date": order.order_date
            }
            for order in orders
        ]

    @staticmethod
    def get_order_by_id(order_id, user_id):

        print(order_id)
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            raise NotFoundError(f"Order with ID '{order_id}' not found for user '{user_id}'")

        return {
            "id": order.id,
            "address": order.address,
            "total_price": order.total_price,
            "status": order.status,
            "order_date": order.order_date,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price
                }
                for item in order.items
            ]
        }
