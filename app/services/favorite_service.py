from app import db
from app.models.favorite import Favorite
from app.models.product import Product
from app.utils.error_handler import ConflictError, BadRequestError, NotFoundError


class FavoriteService:
    @staticmethod
    def add_to_favorites(user_id: str, product_id: str):
        """Добавляет товар в избранное для пользователя"""

        existing_favorite = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()

        if existing_favorite:
            raise ConflictError("Product is already in favorites")

        new_favorite = Favorite(user_id=user_id, product_id=product_id)

        db.session.add(new_favorite)
        db.session.commit()

    @staticmethod
    def get_favorite_products(user_id):
        try:
            favorites = (
                db.session.query(Product)
                .join(Favorite, Favorite.product_id == Product.id)
                .filter(Favorite.user_id == user_id)
                .all()
            )

            return [
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "amount": product.amount,
                }
                for product in favorites
            ]
        except Exception as e:
            raise BadRequestError(f"Error fetching favorite products: {str(e)}")

    @staticmethod
    def delete_favorite(user_id, product_id):
        favorite = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()
        if not favorite:
            raise NotFoundError("Favorite not found")

        try:
            db.session.delete(favorite)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise BadRequestError(f"Error deleting favorite product: {str(e)}")
