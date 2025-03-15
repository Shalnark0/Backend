from app import db
import uuid

class RefreshToken(db.Model):
    __tablename__ = "refresh_token"

    id = db.Column(db.BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes, unique=True, nullable=False)
    user_id = db.Column(db.BINARY(16), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = db.Column(db.Text, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

