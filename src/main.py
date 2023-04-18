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
    tracks = SpotifyAPI().run()
    events = TicketmasterAPI(tracks).run() if tracks else None

    return [event.get("artist") for event in events if event]


if "__main__" == __name__:
    print(search_events())
