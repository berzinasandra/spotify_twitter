"""
Generates Spotify token using Spotify Client ID
and Spotify Client Secret as identifier. 
"""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


def get_token():
    url = "https://accounts.spotify.com/api/token"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(url, headers=header, data=data)
    if 300 > response.status_code >= 200:
        token = response.json().get("access_token")
        return token


if __name__ == "__main__":
    get_token()
