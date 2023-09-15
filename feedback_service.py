from errors import FeedbackNotFoundError
from models import Feedback
from db import session

def create_feedback(feedback_dict: dict):
  feedback = Feedback.from_dict(feedback_dict) 
  session.add(feedback)
  session.commit()
  return feedback
def update_feedback(feedback_dict: dict):
  feedback = session.query(Feedback).get(feedback_dict['id'])
  if not feedback:
    raise FeedbackNotFoundError()
  feedback.title = feedback_dict['title']
  feedback.content = feedback_dict['content']
  session.commit()
  return feedback
def delete_feedback(feedback_id: int):
  feedback = session.get(Feedback, feedback_id)
  if not feedback:
    raise FeedbackNotFoundError()
  session.delete(feedback)
  session.commit()
  return True

def get_feedback_by_id(id: int):
  feedback = session.get(Feedback, id)
  return feedback

def get_feedback_list(limit: int = 10, skip: int = 0):
  return session.query(Feedback).limit(limit).offset(skip).all()