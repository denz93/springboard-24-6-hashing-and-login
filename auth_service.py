from flask import session, request, redirect, g
from auth_lib import secure_hash
from errors import UsernamePasswordInvalidError
from models import User
from user_service import get_user_by_username
from db import db

def login(user: User):
  session.setdefault('user', user.username)

def logout(user: User):
  session.pop('user')

def authenticate(username, password):
  user = get_user_by_username(username)
  if not user:
    raise UsernamePasswordInvalidError()
  hashed_pass = secure_hash(msg=password, salt=user.salt)
  if hashed_pass != user.password:
    raise UsernamePasswordInvalidError()
  return user 

def protect_route(route_func):
  def wrapper(*args, **kargs):
    if 'user' not in session:
      return redirect('/login')
    user = db.session.get(User, session.get('user'))
    if user == None:
      session.pop('user')
      return redirect('/login')
    g.setdefault('user', user)
    return route_func(*args, **kargs)
  wrapper.__name__ = route_func.__name__
  return wrapper

def admin_only(route_func):
  def wrapper(*args, **kargs):
    if 'user' not in session:
      return redirect('/')
    user = db.session.get(User, session.get('user'))
    g.setdefault('user', user)
    if not user.is_admin:
      return redirect('/')
    return route_func(*args, **kargs)
  wrapper.__name__ = route_func.__name__
  return wrapper
  