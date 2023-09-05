import os
import spotipy
from datetime import datetime
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

CALLBACK_URI = os.getenv('SPOTIFY_CALLBACK_URI')

MONTHS = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
        7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

def get_top_songs() -> tuple[str, str]:
    # Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=CALLBACK_URI,
        scope="user-top-read"
    ))

    # get top 10 songs from last 30 days
    top_songs = sp.current_user_top_tracks(time_range="short_term", limit=10)
    top_songs = [(song.get('name', '[Song Name]'), song.get('artists', {'name':'[Artist]'})[0]['name']) for song in top_songs.get('items', [])]

    return top_songs


def get_username() -> str:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=CALLBACK_URI,
        scope="user-top-read"
    ))

    # get user's display name
    user_info = sp.current_user()

    return user_info.get('display_name', '[Your Name]')


def get_messages() -> str:
    """ returns a string of the message to be sent to the user """
    month, year = datetime.now().month, datetime.now().year
    top_songs, name = get_top_songs(), get_username()
    if top_songs is None or name is None:
        return ''
    top_songs = '\n'.join([f'{i+1}. {song[0]} - {song[1]}' for i, song in enumerate(top_songs[:10])])
    return f"Hello there, {name}!\nHere are your top songs from {MONTHS.get(month, month)}, {year}:\n{top_songs}"

if __name__ == '__main__':
    print(get_messages())