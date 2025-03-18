import logging
from app import db
from app.models.favorite import Favorite
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

            existing_product = Product.query.filter_by(name=name).first()
            if existing_product:
                raise BadRequestError(f"Product with name '{name}' already exists")

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
        product.amount = data.get("amount", product.amount)

        try:
            db.session.commit()
            return {"message": "Product updated successfully"}
        except Exception as e:
            db.session.rollback()
            raise BadRequestError(f"Error updating product: {str(e)}").to_response()

    @staticmethod
    def delete_product(product_id):
        product = db.session.get(Product, product_id)
        if not product:
            raise NotFoundError("Product not found").to_response()


        Favorite.query.filter_by(product_id=product_id).delete()

        try:
            db.session.delete(product)
            db.session.commit()
            return {"message": "Product and related favorites deleted successfully"}
        except Exception as e:
            db.session.rollback()
            raise BadRequestError(f"Error deleting product: {str(e)}").to_response()

    @staticmethod
    def get_product(product_id):
        product = db.session.get(Product, product_id)
        if not product:
            raise NotFoundError("Product not found").to_response()

        return {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "amount": product.amount
        }

    @staticmethod
    def get_all_products():

        products = db.session.query(Product).all()

        return [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "amount": product.amount
            } for product in products
        ]
