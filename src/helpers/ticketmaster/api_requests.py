import requests
from requests import Response
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TICKETMASTER")


def request_ticketmaster_endpoint(url: str) -> Response:
    """Call given Ticketmaster API and return request response

    Args:
        service (str): name of the service
        url (str): API URL

    Returns:
        Response: Request response of given service
    """

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    if 300 > response.status_code >= 200:
        return response.json()
