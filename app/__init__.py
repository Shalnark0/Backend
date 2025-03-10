from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/mydb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "secret_key"

    db.init_app(app)

    from app.routes.auth import auth_routes
    from app.routes.register import register_routes
    from app.routes.article import article_routes

    app.register_blueprint(article_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(register_routes)

    return app
