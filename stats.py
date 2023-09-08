import os
# import numpy as np
import spotipy
from statistics import mean
from datetime import datetime
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

CALLBACK_URI = os.getenv('SPOTIFY_CALLBACK_URI')

MONTHS = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
        7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}


def retrieve_top_songs(limit:int=10, sp:spotipy.Spotify=None) -> list[dict]:
    """ returns a list of dictionaries containing the top songs from the last 30 days """
    if sp is None:
        # Spotify client
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=CALLBACK_URI,
            scope="user-top-read"
        ))

    # get top limit songs from last 30 days
    return sp.current_user_top_tracks(time_range="short_term", limit=limit).get('items', [])


def songs_info(songs:list[dict]) -> list[tuple[str, str]]:
    return [(song.get('name', '[Song Name]'), (', '.join([artist.get('name', '[Artist Name]') for artist in song.get('artists', [{}])]))) for song in songs]


def get_avg_popularity(songs:list[dict]) -> float:
    avg_pop = mean([song.get('popularity', None) for song in songs])
    return avg_pop


def get_username(sp:spotipy.Spotify=None) -> str:
    if sp is None:
        # Spotify client
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=CALLBACK_URI,
            scope="user-top-read"
        ))

    # get user's display name
    return sp.current_user().get('display_name', '[Your Name]')


def get_monthly_update() -> str:
    """ returns a string of the monthly update message to be sent to the user """
    month, year = datetime.now().month, datetime.now().year

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=CALLBACK_URI,
        scope="user-top-read"
    ))

    songs = retrieve_top_songs(sp=sp, limit=100)

    top_songs, name, avg_pop = songs_info(songs[:10]), get_username(sp), get_avg_popularity(songs)
    if top_songs is None or name is None:
        return ''
    top_songs = '\n'.join([f'{i}. {song[0]} - {song[1]}' for i, song in enumerate(top_songs[:10], start=1)])
    return f"Hello there, {name}!\nHere are your top songs from {MONTHS.get(month, month)}, {year}:\n{top_songs}\nThis month's Indie Score: {100-int(avg_pop)}."



if __name__ == '__main__':
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(get_monthly_update())