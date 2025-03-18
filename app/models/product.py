from app import db
import uuid

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    photo1 = db.Column(db.String(255), nullable=True)
    photo2 = db.Column(db.String(255), nullable=True)
    photo3 = db.Column(db.String(255), nullable=True)
