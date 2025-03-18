from app import db
import uuid

class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)

    user = db.relationship('User', backref='favorites', lazy=True)
    product = db.relationship('Product', backref='favorites', lazy=True)

