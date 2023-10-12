import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, session, url_for
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import oracledb
from keep_alive import connect_to_database
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["http://localhost"]}})
# cors = CORS(app, resources={r"/*": {"origins": '*'}})

TABLE_NAME = 'user_data'

# Spotify API connection info
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
# SPOTIFY_REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI')
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback/'
sp_auth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-top-read"
)


# Flask info
FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')


@app.route('/')
def index():
    auth_url = sp_auth.get_authorize_url()
    return redirect(auth_url)
    # return "Welcome to the website! Please enter your phone number."

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    token_info = sp_auth.get_access_token(request.args.get('code'))
    session['token_info'] = token_info
    print(token_info)
    # return redirect(url_for('index'))

@app.route('/contains', methods=['GET'])
def contains():
    phone_number = request.args.get('phone_number')
    # phone_number = request.form['phone_number']

    # check if phone number is in database
    with connect_to_database() as connection:
        assert(connection is not None)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE PHONENUMBER = '{phone_number}'")
            result = cursor.fetchone()
            if result is None:
                return "false"
            else:
                return "true"
    


if __name__ == '__main__':
    app.secret_key = FLASK_SECRET_KEY
    app.run(debug=True, port=8888)
