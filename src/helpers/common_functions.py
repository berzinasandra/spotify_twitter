from dotenv import load_dotenv  # pip3 install python-dotenv
import logging
from dataclasses import dataclass
from datetime import datetime
import requests

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
        return items["items"] if service == "spotify" else items


def _unsecessful_request(response, service, items):
    if items is None and response.status_code == 401 and service == "spotify":
        return True
    if response.status_code == 401 and service == "ticketmaster":
        logger.info(f"{service.title()} Token has expired, need to update it!")
        return True
    if response.status_code > 300:
        logger.info(f"FAILED {response.status_code} - {response.text}")
        return True
  

def make_request(
    url: str = None, offset: int = None, service: str = None, spotify_token: str = None
):
    response = _request_endpoint(service, url, offset, spotify_token)

    if _unsecessful_request and service == "spotify":
        logger.info("Creating new token...")
        response = _request_endpoint(service, url, offset, spotify_token)
        if _unsecessful_request:
            logger.info("No response from endpoint")
            return []
    
    items = _retrieve_items(response, service)
    return items


@dataclass
class Artist:
    """
    Formatting data for artists 
    """
    added_at: datetime
    artists: list
    song_name: dict
    images: list
    release_date: str

@dataclass
class Event:
    """
    Formatting data for detected events 
    """
    ticket_type_name: str
    ticket_type_id: str
    ticket_url: list
    concert_date: str
    concert_starting_time: str
    concert_timezone: str
    tikcet_status: str
    genre: list
    promoter_info: dict
    venues: list
    social_media_links: list
