from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import smtplib
from email.message import EmailMessage
import time

#sending an email

def email_alert(subject, body, to):
  msg = EmailMessage()
  msg.set_content(body)
  msg['subject'] = subject
  msg['to'] = to

  user = 'your@mail.com'
  msg['from'] = user
  password = 'yourpassword'

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(user, password)
  server.send_message(msg)

  server.quit()

#bitcoin price track

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '9ce8ef2d-56b6-4f1d-9863-548e2cd2b606',
}

session = Session()
session.headers.update(headers)

while True:
  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    price = data['data'][0]['quote']['USD']['price']
    msg = f'Cijena BitCoin-a trenutno je {price}.'
    email_alert("Trenutna cijena BitCoin-a", msg, 'to@mail.com')

  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
  time.sleep(60)



