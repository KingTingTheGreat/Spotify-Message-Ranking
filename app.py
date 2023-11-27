import os
import random
import string
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, Response, jsonify
from flask_cors import CORS
from database_functions import PRODUCTION_TABLE, num_rows, contains, add_to_table
from spotify_functions import generate_authorization_url

load_dotenv()

# stores a state key and phone number value
state_numbers = {}

FLASK_SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY

cors = CORS(
    app,
    resources={
        r"/*": {
            "origins": ["http://127.0.0.1*", "https://accounts.spotify.com/authorize*"]
        }
    },
)
# cors = CORS(app, resources={r"/*": {"origins": '*'}})


def gen_state(n=16):
    """returns a random string of length n that we use as a state key"""
    return "".join(random.choice(string.ascii_letters) for _ in range(n))


@app.route("/")
def index():
    # auth_url = sp_auth.get_authorize_url()
    return redirect("https://kingtingthegreat.github.io/Spotify-Message-Ranking/")
    return "Welcome to the website! Please enter your phone number."


@app.route("/callback", methods=["GET"])
def callback():
    print(state_numbers)
    auth_code = request.args.get("code", None)
    # session['token_info'] = token_info
    print(f"AUTH CODE: {auth_code}")
    state = request.args.get("state", None)
    print(f"STATE: {state}")
    phone_number = state_numbers.pop(request.args.get("state", None), None)
    print(f"PHONE NUMBER: {phone_number}")

    if auth_code is None or phone_number is None:
        return Response(
            "Error: invalid auth code or phone number",
            status=400,
            mimetype="application/json",
        )

    add_to_table(PRODUCTION_TABLE, phone_number, auth_code)

    # redirect to front end homepage; will be changed in the future
    return redirect("http://127.0.0.1:5500/index.html")
    return redirect("https://kingtingthegreat.github.io/Spotify-Message-Ranking/")


@app.route("/api/signup", methods=["POST"])
def signup():
    print(f"REQUEST ARGS: {request.args}")
    # get input phone number
    phone_number = request.args.get("phone_number", None)
    # data = request.get_data().decode('utf-8')
    # print(f'DATA: {data}')
    print(f"PHONE NUMBER: {phone_number}")

    # already signed up, tell user this
    if phone_number is None or contains(PRODUCTION_TABLE, phone_number):
        print("Already signed up")
        return Response("Already signed up!", status=400, mimetype="application/json")

    # store phone number in hashtable temporarily
    print("New user, adding to database")
    state = gen_state()
    state_numbers[state] = phone_number

    # redirect to spotyify auth page
    redir = generate_authorization_url(state)
    print(f"REDIR: {redir}")
    return jsonify({"redirect": redir})
    return redirect(redir)
    # return redirect(generate_authorization_url(state))


if __name__ == "__main__":
    # add_to_database('1234567890')
    print(f"Num Users: {num_rows(PRODUCTION_TABLE)}")
    app.secret_key = FLASK_SECRET_KEY
    app.run(debug=True, port=8888)
