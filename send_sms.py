import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID:str = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN:str = os.getenv('TWILIO_AUTH_TOKEN')
NUMBER:int = int(os.getenv('TWILIO_NUMBER'))
assert ACCOUNT_SID is not None and AUTH_TOKEN is not None

client:Client = Client(ACCOUNT_SID, AUTH_TOKEN)

message_body = input('Enter your message: ')
# destination_number = input('+19177575886')
destination_number = '+19177575886'

message = client.messages.create(body=message_body, from_=NUMBER, to=destination_number)
print(message.sid)