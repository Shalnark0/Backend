from app import db
from sqlalchemy import JSON
import uuid

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(80), default="user")
    is_active = db.Column(db.Boolean, default=True)
    avatar = db.Column(JSON, nullable=True, default=list)
