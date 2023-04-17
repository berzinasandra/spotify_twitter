import logging
import json
from spotify import SpotifyAPI
from ticketmaster import TicketmasterAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MAIN")
logger.setLevel(logging.INFO)

def search_events():
    tracks = SpotifyAPI().run()
    events = TicketmasterAPI(tracks).run() if tracks else None
    
    logger.info(f"FOUND EVENTS FOR ARTIST \n {[event.get('artist') for event in events if event]}")
    # return events

if '__main__' == __name__:
    print(search_events())

# TODO: 
# in case not in Amsterdam, look for Europe
