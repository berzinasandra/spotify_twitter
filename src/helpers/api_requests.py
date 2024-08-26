from dotenv import load_dotenv  # pip3 install python-dotenv
import logging

import requests
import os
from dotenv import load_dotenv
from helpers.utils import save_as_parquet
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("REQUESTS")
logger.setLevel(logging.INFO)

load_dotenv()


def _make_spotify_request(url, offset, spotify_token):
    token = spotify_token
    header = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.get(url + str(offset), headers=header)
    return response


def _request_endpoint(service, url, offset, spotify_token):
    if service == "spotify":
        response = _make_spotify_request(url, offset, spotify_token)
    elif service == "ticketmaster":
        response = requests.get(url)
    return response


def _retrieve_items(response, service):
    if 300 > response.status_code >= 200:
        items = response.json()
        return items['tracks']['items'] if service == 'spotify' else items


def _unsecessful_request(response, service):
    if response.status_code == 401 and service == "ticketmaster":
        logger.info(f"{service.title()} Token has expired, need to update it!")
        return True
    elif response.status_code > 300:
        logger.info(f"FAILED {response.status_code} - {response.text}")
        return True
    

def get_token() -> None:
    """
    Generates Spotify token using Spotify Client ID
    and Spotify Client Secret as identifier. 
    """
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



def make_request(
    url: str = None, offset: int = None, service: str = None, spotify_token: str = None
):
    import pandas as pd
    from helpers.variables import SPOTIFY_RAW_DATA_PATH, TICKETMASTER_RAW_DATA_PATH

    response = _request_endpoint(service, url, offset, spotify_token)
    if _unsecessful_request(response, service) and service == "spotify":
        logger.info("Creating new token...")
        response = _request_endpoint(service, url, offset, spotify_token)
        if _unsecessful_request(response, service) :
            logger.info("No response from endpoint")
            return []
    
    items = _retrieve_items(response, service)
    items_df = pd.DataFrame(items)
    if service == "spotify":
        output_path = f"{SPOTIFY_RAW_DATA_PATH}/spotify_{offset}.parquet"
    else:
        output_path = f"{TICKETMASTER_RAW_DATA_PATH}/ticketmaster_{offset}.parquet"
        
    save_as_parquet(items_df, output_path)

if __name__ == "__main__":
    print(get_token())
