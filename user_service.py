from auth_lib import secure_hash, generate_salt
from errors import UserNotFoundError, UsernameOrEmailExistingError
from models import User
from db import session
from sqlalchemy import or_
def create_user(user_dict: dict):
  email_or_username_filter = or_(
    User.email == user_dict['email'],
    User.username == user_dict['username']
  )
  user = session.query(User).filter(email_or_username_filter).first()
  if user: 
    raise UsernameOrEmailExistingError()
  user = User(**user_dict)
  user.salt = generate_salt()
  user.password = secure_hash(user.password, user.salt)
  session.add(user)
  session.commit()
  return user

def get_user_by_username(username: str) -> User:
  return session.get(User, username, populate_existing=True) 

def delete_user(username):
  user = session.query(User).filter(User.username == username).first()
  if not user:
    raise UserNotFoundError()
  
  session.delete(user)
  session.commit()

def create_admin_user():
  admin = get_user_by_username('admin')
  if admin:
    return admin
  salt = generate_salt()
  hashed_password = secure_hash('admin', salt)
  admin = User(
    username='admin', 
    password=hashed_password, 
    is_admin=True, 
    email='admin@localhost', 
    last_name='nhan', 
    first_name='bach', 
    salt=salt)
  session.add(admin)
  session.commit()
  return admin

def get_user_list(limit: int = 10, skip: int = 0):
  return session.query(User).limit(limit).offset(skip).all()