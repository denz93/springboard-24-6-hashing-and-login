from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.types import Integer, String, Text, DateTime, Boolean
from sqlalchemy import Column, ForeignKey
from typing import List
import inspect
from datetime import datetime
class Base(DeclarativeBase):
  def to_dict(self):
    attrs = inspect.get_annotations(self.__class__)
    json = {}
    for attr in attrs.keys():
      value = getattr(self, attr)
      if attr == 'feedbacks':
        feedbacks = []
        for f in value:
          feedbacks.append(f.to_dict())
        value = feedbacks
      json[attr] = value
    return json
  @classmethod
  def from_dict(cls, data):
    obj = cls()
    attrs = inspect.get_annotations(cls)
    for key, value in data.items():
      if key in attrs:
        if key == 'feedbacks':
          obj.feedbacks = [Feedback.from_dict(f) for f in value]
        else:
          setattr(obj, key, value)
    return obj
  
class User(Base):
  __tablename__ = 'users'
  username: Mapped[String] = Column(String(20), primary_key=True)
  password: Mapped[String] = Column(String(128), nullable=False)
  email: Mapped[String] = Column(String(50), nullable=False, unique=True)
  first_name: Mapped[String] = Column(String(30), nullable=False)
  last_name: Mapped[String] = Column(String(30), nullable=False)
  feedbacks: Mapped[List["Feedback"]] = relationship("Feedback", backref="user", cascade="all, delete-orphan", lazy="select")
  salt: Mapped[String] = Column(String(64), nullable=False)
  is_admin: Mapped[bool] = Column(Boolean, default=False)
  password_resets: Mapped[List["PasswordReset"]] = relationship("PasswordReset", backref="user", cascade="all, delete-orphan", lazy="select")

class Feedback(Base):
  __tablename__ = 'feedbacks'
  id: Mapped[Integer] = Column(Integer, autoincrement=True, primary_key=True)
  title: Mapped[String] = Column(String(100), nullable=False)
  content: Mapped[String] = Column(Text(), nullable=False)
  username: Mapped[String] = Column(String, ForeignKey("users.username"), nullable=False)

class PasswordReset(Base):
  __tablename__ = 'password_resets'
  id: Mapped[Integer] = Column(Integer, autoincrement=True, primary_key=True)
  code: Mapped[String] = Column(String(6), nullable=False)
  is_used: Mapped[bool] = Column(Boolean, default=False)
  created_at: Mapped[DateTime] = Column(DateTime, default=datetime.utcnow, nullable=False)
  username: Mapped[String] = Column(String, ForeignKey("users.username"), nullable=False)
