from app import db
import uuid
import sqlalchemy.dialects.mysql as mysql

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(mysql.BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    photo1 = db.Column(db.String(255), nullable=True)
    photo2 = db.Column(db.String(255), nullable=True)
    photo3 = db.Column(db.String(255), nullable=True)