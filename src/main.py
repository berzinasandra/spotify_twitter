"""
Main file to run the event finder
"""

import logging
from spotify import SpotifyAPI
from ticketmaster import TicketmasterAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MAIN")
logger.setLevel(logging.INFO)


def search_events():
    """
    First gets all artists that all in Stared and Shazam playlist.

    Returns:
        list: list of events
    """
    SpotifyAPI().run()
    TicketmasterAPI().run()


# Add cash to Spotify api
# Check when last time playlist was updated
# Add linting
# Add docstrings and formatting
# Move .env to github secrets
# test
# alembic

if "__main__" == __name__:
    print(search_events())
