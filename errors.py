class Error(Exception):
  code: int = 0
  message: str = "general error"
  http_code: int = 400
  def __init__(self, message=None, code=None, http_code=None):
    if message is not None:
      self.message = message
    if code is not None:
      self.code = code
    if http_code is not None:
      self.http_code = http_code

class ClientError(Error):
  http_code = 404

class UserExistError(ClientError):
  code = 404
  message = "User already exists"

class UserNotFoundError(ClientError):
  code = 404
  message = "User not found"

class UsernamePasswordInvalidError(ClientError):
  code = 404
  message = "Username or Password incorrect"
  
class FeedbackNotFoundError(ClientError):
  code = 404
  message = "Feedback not found"

class PasswordResetExpiredError(ClientError):
  code = 404
  message = "Password reset expired"

class PasswordResetWrongCodeError(ClientError):
  code = 404
  message = "Wrong password reset code"

class UsernameOrEmailExistingError(ClientError):
  code = 404
  message = "Username or email already exists"