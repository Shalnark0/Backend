from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DATABASE_URL = 'mysql+pymysql://root:root@localhost/mydb'


def get_db():
    db_session = db.session()
    try:
        yield db_session
    finally:
        db_session.close()
