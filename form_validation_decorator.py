from typing import Type
from wtforms import Form
from flask import g, request, flash

def validate_form(formCls: Type[Form]):
  def decorator(route_func):
    def wrapper(*args, **kargs):
      form = formCls(request.form)
      if form.validate() :
        g.setdefault('form', form)
      else:
        for field_name, error_list in form.errors.items():
          flash(f"{field_name}: {error_list[0]}", 'error')
      return route_func(*args, **kargs)
    wrapper.__name__ = route_func.__name__
    return wrapper
  return decorator