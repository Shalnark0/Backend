from app import db
from app.models.favorite import Favorite
from app.utils.error_handler import ConflictError

class FavoriteService:
    @staticmethod
    def add_to_favorites(user_id: bytes, product_id: bytes):
        """Добавляет товар в избранное для пользователя"""

        existing_favorite = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing_favorite:
            raise ConflictError("Product is already in favorites")

        new_favorite = Favorite(user_id=user_id, product_id=product_id)
        db.session.add(new_favorite)
        db.session.commit()
