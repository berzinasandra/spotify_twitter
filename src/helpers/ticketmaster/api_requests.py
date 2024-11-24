import functools
import logging

import requests
from requests import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TICKETMASTER")


@functools.cache
def request_ticketmaster_endpoint(url: str, session: Session) -> dict:
    """Call given Ticketmaster API and return request response

    Args:
        url (str): API URL
        session: requests session

    Returns:
        Response: Request response as a json
    """

    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    if 300 > response.status_code >= 200:
        return response.json()
