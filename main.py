import os
import time
from datetime import datetime
from stats import get_messages
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID:str = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN:str = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER:str = os.getenv('TWILIO_NUMBER')

def is_last_day_of_month() -> bool:
    """ returns a boolean representing whether it is the last day of the month """
    day, month, year = datetime.now().day, datetime.now().month, datetime.now().year
    if month == 2:
        if year % 4 == 0:
            return day == 29
        else:
            return day == 28
    elif month in [4, 6, 9, 11]:
        return day == 30
    else:
        return day == 31
    

def send_message(message:str) -> None:
    """ sends a message to the user """
    c = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = c.messages.create(body='a message was received', from_=TWILIO_NUMBER, to='')


def main():
    last_month_sent = datetime.now().month - 1  # ensures we send a message at the end of the current month
    while True:
        if not is_last_day_of_month() or last_month_sent == datetime.now().month:
            time.sleep(60)
            continue
        last_month_sent = datetime.now().month
        messages = get_messages()
        if not messages:
            time.sleep(60)
            continue
        for message in messages:
            if not message:
                continue
            send_message(message)
        time.sleep(60)




if __name__ == '__main__':
    main()
