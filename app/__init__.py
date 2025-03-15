from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.utils.error_handler import Error

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/mydb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "secret_key"

    db.init_app(app)

    from app.routes.auth import auth_routes
    from app.routes.register import register_routes
    from app.routes.product import product_routes
    from app.routes.order import order_routes

    app.register_blueprint(order_routes)
    app.register_blueprint(product_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(register_routes)

    @app.errorhandler(Error)
    def handle_app_error(error):
        return error.to_response()

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        print(f"Unexpected error: {error}")
        return jsonify({"error": "Internal Server Error"}), 500

    return app
