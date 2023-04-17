import requests
from dotenv import load_dotenv  # pip3 install python-dotenv
import logging
import os
from dataclasses import dataclass
from datetime import datetime

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


def _check_response(response, service, items):
    respose_good = False
    if items is None and response.status_code == 401 and service == "spotify":
        return False
    elif response.status_code == 401 and service == "ticketmaster":
        logger.info(f"{service.title()} Token has expired, need to update it!")
        return False
    else:
        print(f"FAILED {response.status_code} - {response.text}")


def make_request(
    url: str = None, offset: int = None, service: str = None, spotify_token: str = None
):
    response = _request_endpoint(service, url, offset, spotify_token)
    items = _retrieve_items(response, service)

    if not _check_response and service == "spotify":
        print("Create new token")
        response = _request_endpoint(service, url, offset, spotify_token)
        items = _retrieve_items(response, service)
        if not _check_response:
            print("NO response")
            return []
    elif _check_response:
        return items


@dataclass
class Artist:
    added_at: datetime
    artists: list
    song_name: dict
    images: list
    release_date: str


@dataclass
class Event:
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
