import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
ACCOUNT_SID:str = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN:str = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER:str = os.getenv('TWILIO_NUMBER')
DEST_NUMBER:str = os.getenv('DEST_NUMBER')

app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def incoming_sms():
    # body = request.values.get('Body', None)
    # resp = MessagingResponse()
    # if body is None:
    #     return ''
    # resp.message(f'You said: {body}')

    client:Client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(body='a message was received', from_=TWILIO_NUMBER, to=DEST_NUMBER)
    # message = client.messages.create(body=f'Message: {body}', from_=TWILIO_NUMBER, to=DEST_NUMBER)


@app.route('/callback')
def callback():
    authorization_code = request.args.get('code')
    # store code in database
    return 'Authorization code successfully stored'


# create function to store data in database


if __name__ == '__main__':
    print('Starting Flask app')
    c = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = c.messages.create(body='starting Flask application!', from_=TWILIO_NUMBER, to=DEST_NUMBER)
    del c, message
    app.run(debug=True)