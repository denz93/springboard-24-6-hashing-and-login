import requests
from config import config
from logging import getLogger
BASE_URL = f'https://api.mailgun.net/v3/{config.MAILGUN_DOMAIN}'

log = getLogger('gunicorn.error')
def send_email(title: str, body: str, to: str):
  try:
    log.info(f'Sending email to {to}: {title}')
    res = requests.post(
      url=BASE_URL + '/messages',
      auth=('api', config.MAILGUN_KEY),
      data={
        'from': config.MAILGUN_SENDER_EMAIL,
        'to': to,
        'subject': title,
        'text': body
      }
    )
    if res.status_code != 200:
      log.warn(f'Error sending email to {to}: {res.text}', extra={'status_code': res.status_code})
      log.warn(f"Mailgun sender: ${config.MAILGUN_SENDER_EMAIL}")
      log.warn(res)
  except Exception as e:
    log.warn(f'Error sending email to {to}: {e}')

if __name__ == '__main__':
  send_email('test', 'test', 'voanhkiem6@gmail.com')