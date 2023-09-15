from os import getenv
import dotenv
dotenv.load_dotenv()

class Config:
  DATABASE_URI= getenv('DATABASE_URI', None)
  ENV=None
  SECRET=getenv('SECRET', None)
  MAILGUN_KEY = getenv('MAILGUN_KEY', None)
  MAILGUN_DOMAIN = getenv('MAILGUN_DOMAIN', None)
  MAILGUN_SENDER_EMAIL = getenv('MAILGUN_SENDER_EMAIL', None)

class DevConfig(Config):
  ENV='DEV'
  DATABASE_URI='postgresql://localhost/hashing_and_login'
  SECRET='123'

class ProdConfig(Config):
  ENV='PROD'
  
def load_config() -> Config:
  env = getenv('ENV', 'DEV')
  print(f"Loading config for {env} environment")
  if env == DevConfig.ENV:
    return DevConfig()
  elif env == ProdConfig.ENV:
    return ProdConfig()
  raise f"ENV environment not set. Must be either {DevConfig.ENV}, {ProdConfig.ENV}"

config = load_config()