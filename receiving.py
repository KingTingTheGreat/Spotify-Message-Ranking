import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def sms_print():
    body = request.values.get('Body', None)
    if body is None:
        return ''
    
    response = MessagingResponse()
    response.message(f'You said: {body}')
    # response.message('Hello from Twilio!')
    # print(str(response))
    print(response)
    print(str(response))
    
    ACCOUNT_SID:str = os.getenv('TWILIO_ACCOUNT_SID')
    AUTH_TOKEN:str = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_NUMBER:str = os.getenv('TWILIO_NUMBER')
    DEST_NUMBER:str = os.getenv('DEST_NUMBER')
    assert ACCOUNT_SID is not None and AUTH_TOKEN is not None

    client:Client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(body=f'Message: {body}', from_=TWILIO_NUMBER, to=DEST_NUMBER)

if __name__ == '__main__':
    print('Starting Flask app')
    app.run(debug=True)