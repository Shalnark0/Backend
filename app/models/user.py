from app import db
import uuid
import sqlalchemy.dialects.mysql as mysql

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(mysql.BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(80), default="user")
    is_active = db.Column(db.Boolean, default=True)