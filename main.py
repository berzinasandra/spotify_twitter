import logging
from spotify import SpotifyAPI
from ticketmaster import TicketmasterAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MAIN")
logger.setLevel(logging.INFO)

def search_events():
    tracks = SpotifyAPI().run()
    events = TicketmasterAPI(tracks).run() if tracks else None
    
    # logger.info(f"FOUND EVENTS FOR ARTIST \n {[event.get('artist') for event in events if event]}")
    return [event.get('artist') for event in events if event]

if '__main__' == __name__:
    print(search_events())
