from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_db():
    try:
        db.create_all()
        print("postgres connected")
    except Exception as e:
        print(e)    