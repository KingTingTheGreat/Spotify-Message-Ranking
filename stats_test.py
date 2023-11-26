import os
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv
from stats import get_username

load_dotenv()
ACCOUNT_SID:str = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN:str = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER:str = os.getenv('TWILIO_NUMBER')
DEST_NUMBER:str = os.getenv('DEST_NUMBER')

MONTHS = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
        7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

month, year = datetime.now().month, datetime.now().year

top_songs, name = get_username()
assert top_songs is not None and name is not None

top_songs:str = '\n'.join([f'{i+1}. {song[0]} - {song[1]}' for i, song in enumerate(top_songs[:10])])
message = \
        f"Hello there, {name}!\nHere are your top songs from {MONTHS.get(month, month)}, {year}:\n{top_songs}"
print(message)

# c = Client(ACCOUNT_SID, AUTH_TOKEN)
# message = c.messages.create(body=message, from_=TWILIO_NUMBER, to=DEST_NUMBER)