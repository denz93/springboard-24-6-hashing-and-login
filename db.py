from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config
from models import Base
db = SQLAlchemy(metadata=Base.metadata)

session = db.session
def db_init(app:Flask):
  app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
  db.init_app(app)

  with app.app_context():
    db.create_all()
