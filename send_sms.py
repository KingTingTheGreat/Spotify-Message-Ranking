import os,sys
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID:str = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN:str = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER:str = int(os.getenv('TWILIO_NUMBER'))
DEST_NUMBER:str = int(os.getenv('DEST_NUMBER'))

assert ACCOUNT_SID is not None and AUTH_TOKEN is not None

client:Client = Client(ACCOUNT_SID, AUTH_TOKEN)

message_body = input('Enter your message: ')

message = client.messages.create(body=message_body, from_=TWILIO_NUMBER, to=DEST_NUMBER)
print(message.status)