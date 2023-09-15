from app import app
from db import db_init, session
from user_service import create_admin_user

def create_app():
  db_init(app)   
  with app.app_context():
    create_admin_user() 
    session.flush()
  return app