import os
import time
from stats import get_username, get_monthly_update
from datetime import datetime
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID:str = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN:str = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER:str = os.getenv('TWILIO_NUMBER')

DEST_NUMBER = os.getenv('DEST_NUMBER')

def is_last_day_of_month() -> bool:
    """ returns a boolean representing whether it is the last day of the month """
    return True
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
    

def send_message(message:str, phone_number:str) -> None:
    """ sends a message to the user """
    c = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    msg = get_monthly_update()
    message = c.messages.create(body=msg, from_=TWILIO_NUMBER, to=phone_number)


def send_welcome(phone_number:str) -> None:
    """ sends a welcome message to the user when they first join """
    c = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    name = get_username()
    msg = f'Welcome, {name}! You have signed up to receive monthly updates on your Spotify listening habits. \nText STOP at any time to no longer receive these updates. MSG & Data rates may apply.'
    message = c.messages.create(body=msg, from_=TWILIO_NUMBER, to=phone_number)


def main():
    last_month_sent = datetime.now().month - 1  # ensures we send a message at the end of the current month
    while True:
        if not is_last_day_of_month() or last_month_sent == datetime.now().month:
            time.sleep(60)
            continue
        last_month_sent = datetime.now().month
        messages = get_monthly_update()
        if not messages:
            time.sleep(60)
            continue
        for message in messages:
            if not message:
                continue
            send_message(message, DEST_NUMBER)
        time.sleep(60)


if __name__ == '__main__':
    # main()
    send_welcome(DEST_NUMBER)
