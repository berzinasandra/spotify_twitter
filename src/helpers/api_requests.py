from dotenv import load_dotenv  # pip3 install python-dotenv
import logging
from typing import Any
import requests
from requests import Response
import os
from dotenv import load_dotenv
from helpers.utils import save_as_parquet
load_dotenv()
import functools

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("REQUESTS")
logger.setLevel(logging.INFO)

load_dotenv()


def _make_spotify_request(url:str, offset:int, spotify_token:str) -> Response:
    """Make a request to Spotify API

    Args:
        url (str): URL of Spotify API
        offset (int): offset of the items to return
        spotify_token (str): spotify token

    Returns:
        Response: Spotify request resposne
    """
    token = spotify_token
    header = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return requests.get(url + str(offset), headers=header)


def _request_endpoint(service:str, url:str, offset:int, spotify_token:str) -> Response:
    """Call given service API and return request response

    Args:
        service (str): name of the service
        url (str): API URL
        offset (int): offset of the items to return
        spotify_token (str): Spotify token

    Returns:
        Response: Request response of given service
    """
    if service == "spotify":
        response = _make_spotify_request(url, offset, spotify_token)
    elif service == "ticketmaster":
        response = requests.get(url)
    return response

@functools.cache
def _retrieve_items(response:Response, service:str) -> list[dict[Any, Any]]:
    """Fetch data from API response 

    Args:
        response (Response): API call's resposne
        service (str): service name

    Returns:
        list[dict[Any, Any]]: retrieved items of responce
    """
    if 300 > response.status_code >= 200:
        items = response.json()
        import pdb;pdb.set_trace()
        return items['tracks']['items'] if service == 'spotify' else items


def _unsecessful_request(response: Response, service:str) -> bool:
    """Checks if response status has been unsecessful

    Args:
        response (Response): API call's resposne
        service (str): service name

    Returns:
        bool: returns True if resposne status is unsecessful
    """
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


def retrieve_data(
    url: str = None, offset: int = None, service: str = None, spotify_token: str = None
) -> None:
    """Retrieve data from given service API and save it locally 

    Args:
        url (str, optional): API URL. Defaults to None.
        offset (int, optional): offset of the items to return. Defaults to None.
        service (str, optional): service name. Defaults to None.
        spotify_token (str, optional): Spotify token. Defaults to None.

    Returns:
        None, writes to disk
    """
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
