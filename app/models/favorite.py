from app import db
import uuid
import sqlalchemy.dialects.mysql as mysql

class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(mysql.BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes, unique=True, nullable=False)
    user_id = db.Column(mysql.BINARY(16), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(mysql.BINARY(16), db.ForeignKey('products.id'), nullable=False)

    user = db.relationship('User', backref='favorites', lazy=True)
    product = db.relationship('Product', backref='favorites', lazy=True)
