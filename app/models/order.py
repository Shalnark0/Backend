from app import db
import uuid
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False)
    total_price = db.Column(db.DECIMAL(10, 2), nullable=False, default=0.00)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))

    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order {self.id}, User {self.user_id}, Status {self.status}, Total Price {self.total_price}>"

class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)

    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

    def __repr__(self):
        return f"<OrderItem {self.id}, Product {self.product_id}, Quantity {self.quantity}, Price {self.price}>"
