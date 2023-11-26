import os
from dotenv import load_dotenv
from database_functions import get_rows, PRODUCTION_TABLE
import requests

load_dotenv()

# spotify API connection info
SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
# SPOTIFY_REDIRECT_URI = os.environ['SPOTIFY_REDIRECT_URI']
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:8888/callback'  # for testing

API_URL = 'https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50'

def generate_authorization_url(state:str) -> str:
    """ returns the authorization url for Spotify API """
    scope = 'user-top-read'
    params = {
        'response_type': 'code',
        'client_id': SPOTIFY_CLIENT_ID,
        'scope': scope,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'state': state, 
        # 'show_dialog': 'true', 
        # 'header': 'application/json', 
        # 'mode': 'no-cors'
        # 'Access-Control-Allow-Credentials': 'true',
        # 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        # 'Access-Control-Allow-Origin': '*'
    }
    return 'https://accounts.spotify.com/authorize?' + '&'.join([f'{key}={value}' for key, value in params.items()])

def do_for_all_users() -> None:
    for auth_code, phone_number in get_rows(PRODUCTION_TABLE):
        print(auth_code, phone_number)
        response = requests.get(API_URL, headers={'Authorization': f'Bearer {auth_code}'})
        print(response.status_code)
        break

def get_username(auth_code: str) -> str: 
    pass

def get_top_songs(auth_code: str) -> list[dict]:
    pass

def get_indie_score(auth_code: str) -> int:
    pass

if __name__ == '__main__':
    # do_for_all_users()
    # auth_url = 'https://accounts.spotify.com/api/token'
    auth_url = generate_authorization_url('test') + '&header=application/json&mode=no-cors'
    print(auth_url)
    # token = 'AQAy7thQeuWlLsDr8d-bnCPFmFR5Uk00Fev1efmC7jWY37AWX3yrQ4RAQyDqpfv4HqVlKt4pYJkTr5_hFinjI81oELo63xsbvVJaHJC39ur13LLejDvQ3s6MwlTPW9kdYUiyNOmFszKoQgDAgVBBScnSeBy9a20a3rO8W6LdjfWgbIw82WMA204oRI5i1xVU_g'
    # data = {
    #     'grant_type': 'client_credentials',
    #     # 'code': token,
    #     # 'redirect_uri': SPOTIFY_REDIRECT_URI,
    #     'client_id': SPOTIFY_CLIENT_ID,
    #     'client_secret': SPOTIFY_CLIENT_SECRET
    # }
    auth_response = requests.get(auth_url, headers={'Access-Control-Allow-Origin': '*'})
    access_token = auth_response.json()

    # print(f'ACCESS TOKEN: {access_token}')
    print('code' in str(access_token))

    base_url = 'https://api.spotify.com/v1/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # get top tracks
    top_tracks_url = base_url + 'browse/featured-playlists/?limit=50'

    response = requests.get(top_tracks_url, headers=headers)
    print(response.status_code)
    print(response.json())