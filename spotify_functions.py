import os
from dotenv import load_dotenv

load_dotenv()

# spotify API connection info
SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
# SPOTIFY_REDIRECT_URI = os.environ['SPOTIFY_REDIRECT_URI']
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'  # for testing

def generate_authorization_url(state:str) -> str:
    """ returns the authorization url for Spotify API """
    scope = 'user-top-read'
    params = {
        'response_type': 'code',
        'client_id': SPOTIFY_CLIENT_ID,
        'scope': scope,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'state': state
    }
    return 'https://accounts.spotify.com/authorize?' + '&'.join([f'{key}={value}' for key, value in params.items()])
