from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms_print():
    response = MessagingResponse()
    # response.message('Hello from Twilio!')
    # print(str(response))
    print(response)
    return str(response)


if __name__ == '__main__':
    app.run(debug=True)