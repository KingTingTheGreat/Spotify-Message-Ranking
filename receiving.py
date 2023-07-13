import os
from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def sms_print():
    response = MessagingResponse()
    origin_number = response.name
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
    message = client.messages.create(body=f'Message from {origin_number}: {str(response)}', from_=TWILIO_NUMBER, to=DEST_NUMBER)

if __name__ == '__main__':
    print('Starting Flask app')
    app.run(debug=True)