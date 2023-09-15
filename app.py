from flask import Flask, flash, render_template, session, redirect, request, g
from auth_service import admin_only, authenticate, login, logout, protect_route
from email_service import send_email
from errors import ClientError, FeedbackNotFoundError, PasswordResetExpiredError, UserNotFoundError, PasswordResetWrongCodeError
from feedback_form import FeedbackFormCreate, FeedbackFormUpdate
from feedback_service import create_feedback, delete_feedback, get_feedback_by_id, get_feedback_list, update_feedback
from form_validation_decorator import validate_form
from password_reset_code_generate_form import PasswordResetCodeGenerateForm
from password_reset_form import PasswordResetForm
from password_reset_service import generate_password_reset_code, is_password_reset_expired, reset_password
from register_form import RegisterForm
from login_form import LoginForm
from models import PasswordReset, User
from user_service import create_admin_user, create_user, delete_user, get_user_by_username, get_user_list 
from config import config
app = Flask(__name__)
app.secret_key = config.SECRET

@app.errorhandler(ClientError)
def handle_client_error(error):
  return render_template('error.html', error=error), error.http_code


@app.context_processor
def bind_user_to_context():
  if 'user' in session:
    return {'user': g.get('user')}
  return {}

@app.get('/')
def home_route():
  if 'user' in session:
    username = session.get('user')
    return redirect(f'/users/{username}')
  return redirect('/register')

@app.get('/register')
def register_route():
  form = RegisterForm()
  if 'user' in session:
    return redirect(f'/users/{session.get("user")}')
  return render_template('register.html', form=form)

@app.get('/login')
def login_route():
  form = LoginForm()
  if 'user' in session:
    return redirect(f'/users/{session.get("user")}')
  return render_template('login.html', form=form)

@app.get('/users/<username>')
@protect_route
def profile_route(username):
  if username != g.get('user').username:
    raise ClientError('You are not allowed to view this profile', http_code=403)
  return render_template('user.html')

@app.get('/users/<username>/feedback/add')
@protect_route
def add_feedback_route(username):
  form = FeedbackFormCreate() 
  if username != g.get('user').username:
    raise ClientError('You are not allowed to view this profile', http_code=403)
  return render_template('create-feedback.html', form=form)

@app.get('/feedbacks/<int:feedback_id>/update')
@protect_route
def update_feedback_route(feedback_id: int):
  feedback = get_feedback_by_id(feedback_id)
  if not feedback:
    raise FeedbackNotFoundError()
  if feedback.username != g.get('user').username:
    raise ClientError('You are not allowed to update this feedback', http_code=403)
  
  form = FeedbackFormUpdate(obj=feedback)
  return render_template('update-feedback.html', form=form, feedback=feedback)

@app.get('/password/reset/confirm/<int:request_id>')
def password_reset_route(request_id: int):
  form = PasswordResetForm()
  return render_template('password-reset.html', id=request_id, form=form)

@app.post('/password/reset/confirm/<int:request_id>')
@validate_form(PasswordResetForm)
def password_reset_post_route(request_id: int):
  form = g.get('form')
  if not form: 
    return render_template('password-reset.html', id=request_id, form = form)
  try:
    reset_password(request_id, form.data['code'], form.data['new_password'])
  except PasswordResetWrongCodeError:
    flash('Wrong password reset code', 'error')
    return render_template('password-reset.html', id=request_id, form=form)
  flash('Password reset successful', 'success')
  return redirect('/login')

@app.get('/password/reset')
def generate_code_for_password_reset_route():
  form = PasswordResetCodeGenerateForm()
  return render_template('password-reset-code-generate.html', form=form) 

@app.post('/password/reset')
@validate_form(PasswordResetCodeGenerateForm)
def generate_code_for_password_reset_post_route():
  form:PasswordResetCodeGenerateForm = g.get('form')
  if not form:
    return render_template('password-reset-code-generate.html', form=PasswordResetCodeGenerateForm(request.form))
  form_data = form.data
  try:
    passwrod_reset = generate_password_reset_code(
      form_data.get('username') or form_data.get('email')
    )
    code = passwrod_reset.code
    if config.ENV != 'PROD':
      print(f'Reset password code: {code}')
    else:
      email = passwrod_reset.user.email
      send_email(
        title='Password reset code', 
        body=f'Your password reset code is: {code}', 
        to=email)
    return redirect(f'/password/reset/confirm/{passwrod_reset.id}')
  except UserNotFoundError:
    flash(f'Cannot find user with provided username or email', 'error')
    return render_template('password-reset-code-generate.html', form=form)




@app.post('/register')
@validate_form(RegisterForm)
def register_post_route():
  form: RegisterForm = g.get('form')
  if not form:
    return render_template('register.html', form=RegisterForm(request.form)), 404
  form_data = {key: value for key, value in form.data.items() if key in ['username', 'password', 'email', 'first_name', 'last_name']}
  user = create_user(form_data)
  login(user)
  return redirect(f'/users/{user.username}')

@app.post('/login')
@validate_form(LoginForm)
def login_post_route():
  form: LoginForm = g.get('form')
  if not form:
    return render_template('/login', form=LoginForm(request.form))
  data = form.data
  try:
    user = authenticate(data['username'], data['password'])
    login(user)
    return redirect(f"/users/{user.username}")
  except ClientError as e:
    flash(e.message, 'error')
    return render_template('login.html', form=LoginForm(request.form))

@app.post('/logout')
def logout_post_route():
  user: User = session.get('user')
  if user:
    logout(user)
  return redirect('/login')

@app.post('/users/<username>/feedback/add')
@validate_form(FeedbackFormCreate)
@protect_route
def add_feedback_post_route(username):
  form: FeedbackFormCreate = g.get('form')
  user: User = g.get('user')
  if not form:
    return render_template('create-feedback.html', form=FeedbackFormCreate(request.form), user=user)
  try:
    data = {**form.data, 'username': user.username}
    feedback = create_feedback(data)
    flash(f'Feedback created "{feedback.title}"', 'success')
    return render_template('create-feedback.html', form=FeedbackFormCreate())
  except ClientError as e:
    flash(e.message, 'error')
    return render_template('create-feedback.html', form=FeedbackFormCreate(request.form))

@app.post('/feedbacks/<int:feedback_id>/update')
@validate_form(FeedbackFormUpdate)
@protect_route
def update_feedback_post_route(feedback_id: int):
  feedback = get_feedback_by_id(feedback_id)
  if not feedback:
    raise FeedbackNotFoundError()
  if feedback.username != g.get('user').username and g.get('user').username != 'admin':
    raise ClientError('You are not the owner of this feedback', 401)
  if 'form' not in g:
    return render_template('update-feedback.html', form=FeedbackFormUpdate(obj=feedback), feedback=feedback)

  form:FeedbackFormUpdate = g.get('form')
  feedback.content = form.data['content']
  feedback.title = form.data['title']
  update_feedback(feedback.to_dict())
  flash(f'Feedback updated "{feedback.title}"', 'success')
  return render_template('update-feedback.html', form=form, feedback=feedback)
  
@app.post('/feedbacks/<int:feedback_id>/delete')
@protect_route
def delete_feedback_post_route(feedback_id: int):
  feedback = get_feedback_by_id(feedback_id)
  if not feedback:
    raise FeedbackNotFoundError()
  if feedback.username != g.get('user').username:
    raise ClientError('You are not the owner of this feedback', 401)
  delete_feedback(feedback_id)
  flash(f'Feedback deleted "{feedback.title}"', 'success')
  return redirect(f'/users/{feedback.username}')

@app.get('/admin/users')
@admin_only
def admin_users_route():
  users = get_user_list(20, 0)
  return render_template('users.html', users=users)

@app.get('/admin/feedbacks')
@admin_only
def admin_feedbacks_route():
  feedbacks = get_feedback_list(20, 0)
  return render_template('feedbacks.html', feedbacks=feedbacks)

@app.post('/admin/users/<username>/delete')
@admin_only
def admin_user_delete_route(username):
  user = get_user_by_username(username)
  if not user:
    raise UserNotFoundError()
  if username == 'admin':
    flash('Cannot delete admin user', 'error')
    return redirect('/admin/users')
  delete_user(user.username)
  flash(f'User "{user.username}" deleted', 'success')
  return redirect('/admin/users')

@app.post('/admin/feedbacks/<int:feedback_id>/delete')
@admin_only
def admin_feedback_delete_route(feedback_id):
  feedback = get_feedback_by_id(feedback_id)
  if not feedback:
    raise FeedbackNotFoundError()
  
  delete_feedback(feedback_id)
  flash(f'Feedback "{feedback.title}" deleted', 'success')
  return redirect('/admin/feedbacks')