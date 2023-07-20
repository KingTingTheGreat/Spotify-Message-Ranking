import os
import spotipy
from datetime import datetime
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

def get_songs_username() -> tuple[str, str]:
    # Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="https://example.com/callback/",
        scope="user-top-read"
    ))

    # get top 10 songs from last 30 days
    top_songs = sp.current_user_top_tracks(time_range="short_term", limit=10)
    top_songs = [(song['name'], song['artists'][0]['name']) for song in top_songs['items']]

    # get user's display name
    user_info = sp.current_user()
    display_name = user_info['display_name']

    return (top_songs, display_name)

def get_message() -> str:
    """ returns a string of the message to be sent to the user """
    month, year = datetime.now().month, datetime.now().year
    top_songs, name = get_songs_username()
    if top_songs is None or name is None:
        return ''
    top_songs = '\n'.join([f'{i+1}. {song[0]} - {song[1]}' for i, song in enumerate(top_songs[:10])])
    return f"Hello there, {name}!\nHere are your top songs from {MONTHS.get(month, month)}, {year}:\n{top_songs}"

if __name__ == '__main__':
    print(get_message())