from datetime import datetime, timedelta
from auth_lib import generate_salt, secure_hash
from db import session
from errors import PasswordResetExpiredError, PasswordResetWrongCodeError, UserNotFoundError
from models import PasswordReset, User
from user_service import get_user_by_username
from sqlalchemy import or_
import os 

def is_password_reset_expired(id: int):
  password_reset = session.get(PasswordReset, id)
  if password_reset:
    return password_reset.created_at < datetime.utcnow() - timedelta(minutes=5) or\
      password_reset.is_used
  return True
def reset_password(id: int, code: str, new_password: str):
  if is_password_reset_expired(id):
    raise PasswordResetExpiredError()
  
  password_reset:PasswordReset = session.query(PasswordReset).get(id)

  if password_reset.code != code.upper():
    raise PasswordResetWrongCodeError()
  new_salt = generate_salt()
  new_password_hash = secure_hash(new_password, new_salt)
  session.query(User)\
    .filter(User.username == password_reset.username)\
    .update({User.password: new_password_hash, User.salt: new_salt})
  password_reset.is_used = True
  session.commit()
  return True

def generate_password_reset_code(username_or_email: str):
  username_or_email_filter = or_(
    User.username == username_or_email,
    User.email == username_or_email
  )
  user = session.query(User).filter(username_or_email_filter).first()
  if not user:
    raise UserNotFoundError()
  
  last_password_reset = session.query(PasswordReset)\
    .filter(
      PasswordReset.username == user.username, 
      PasswordReset.is_used == False,
      PasswordReset.created_at > datetime.utcnow() - timedelta(minutes=5)
      )\
    .order_by(PasswordReset.created_at.asc())\
    .first()
  if last_password_reset:
    return last_password_reset
  
  password_reset = PasswordReset(username=user.username, code=os.urandom(3).hex().upper())
  session.add(password_reset)
  session.commit()
  return password_reset