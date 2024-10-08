"""
Main file to run the event finder
"""

import logging
from ticketmaster import TicketmasterAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MAIN")
logger.setLevel(logging.INFO)


# TODO: upgrade this to something else
def run_event_detector():
    """
    First gets all artists that is in Stared and Shazam playlist.
    """
    # SpotifyAPI().run()
    TicketmasterAPI().run()


# Add cash to Spotify api
# Check when last time playlist was updated
# Add linting
# Add docstrings and formatting
# Move .env to github secrets
# test
# alembic

if "__main__" == __name__:
    print(run_event_detector())
