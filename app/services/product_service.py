import logging
from app import db
from app.models.product import Product
from app.utils.error_handler import BadRequestError, NotFoundError

class ProductService:
    @staticmethod
    def add_product(data):
        try:
            name = data.get("name")
            price = data.get("price")
            amount = data.get("amount")

            if not name or not isinstance(price, (int, float)) or not isinstance(amount, int):
                raise BadRequestError("Invalid input data")

            new_product = Product(
                name=name,
                price=price,
                amount=amount
            )
            db.session.add(new_product)
            db.session.commit()
            return new_product.id
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating product: {str(e)}")
            raise BadRequestError(f"Error creating product: {str(e)}")

    @staticmethod
    def update_product(product_id, data):
        product = db.session.get(Product, product_id)
        if not product:
            raise NotFoundError("Product not found").to_response()

        product.name = data.get("name", product.name)
        product.price = data.get("price", product.price)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise BadRequestError(f"Error updating product: {str(e)}").to_response()
