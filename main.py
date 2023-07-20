import os
import time
from datetime import datetime
from stats import get_message
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID:str = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN:str = os.getenv('TWILIO_AUTH_TOKEN')
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


def main():
    last_month_sent = datetime.now().month - 1
    while True:
        if not is_last_day_of_month() or last_month_sent == datetime.now().month:
            time.sleep(60)
            continue
        last_month_sent = datetime.now().month
        message = get_message()
        if message == '':
            time.sleep(60)
            continue
        c = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = c.messages.create(body=message, from_=TWILIO_NUMBER, to='')
        time.sleep(60)




if __name__ == '__main__':
    main()
