from app import db
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.utils.error_handler import BadRequestError, NotFoundError
from uuid import UUID

class OrderService:
    @staticmethod
    def create_order(data, user_id):

        products = data.get('products')
        address = data.get('address')

        if not products or not address:
            raise BadRequestError("Products and address are required")

        total_price = 0
        order_items = []

        for item in products:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            if not product_id or not quantity:
                raise BadRequestError("Product ID and quantity are required for each item")

            product = Product.query.get(product_id)
            if not product:
                raise NotFoundError(f"Product with ID '{product_id}' not found")

            if product.amount < quantity:
                raise BadRequestError(f"Not enough stock for product '{product.name}'")

            total_price += product.price * quantity
            product.amount -= quantity

            order_items.append(OrderItem(
                product_id=product.id,
                quantity=quantity,
                price=product.price
            ))

        new_order = Order(user_id=user_id, address=address, total_price=total_price, status='pending')
        db.session.add(new_order)
        db.session.flush()

        for item in order_items:
            item.order_id = new_order.id
            db.session.add(item)

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
