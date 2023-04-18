"""
Calls Ticketmaster API endpoint to get event data in Amsterdam
based on the artist that was collected from Spotify playlist API 
and format the data.
"""

import os
import logging
from dotenv import load_dotenv  # pip3 install python-dotenv
from helpers.common_functions import make_request
from helpers.common_functions import Artist, Event

load_dotenv()

TICKETMASTER_KEY = os.getenv("TICKETMASTER_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TICKETMASTER")
logger.setLevel(logging.INFO)


class TicketmasterAPI:
    def __init__(self, tracks: list[Artist]):
        self.tracks = tracks
        self.all_events = []
        self.checked_artists = []

    def run(self):
        for item in self.tracks:
            for artist in item.artists:
                self._find_event(artist)
        return self.all_events

    def _find_event(self, artist: str):
        if artist in self.checked_artists:
            return
        
        self.checked_artists.append(artist)
   
        city = "Amsterdam"
        artist = artist.lower().replace(" ", "_").replace("-", "_")

        url = f"https://app.ticketmaster.com/discovery/v2/events.json?keyword=\
                {artist}&city={city}&apikey={TICKETMASTER_KEY}"
        data = make_request(url, service="ticketmaster")

        if data and data.get("page", dict()).get("totalElements") == 0:
            return

        if data:
            self.parse_data(data, artist)

    def parse_data(self, data: dict, artist: str):
        events = data.get("_embedded", dict()).get("events")
        events_of_artist = self.parse_details(events, artist)
        self.all_events.append({"artist": artist, "concerts": events_of_artist})

    def parse_details(self, events: dict, artist: str):
        parsed = []
        if not events:
            return
        logger.info(f"Found events for artist {artist}")
        for event in events:
            parsed.append(
                Event(
                    event.get("name", None),
                    event.get("id", None),
                    event.get("url", None),
                    event.get("dates", dict())
                    .get("start", dict())
                    .get("localDate", None),
                    event.get("dates", dict())
                    .get("start", dict())
                    .get("localTime", None),
                    event.get("dates", dict()).get("timezone", dict()),
                    event.get("dates", dict()).get("status", dict()).get("code", None),
                    [
                        genre.get("genre")
                        for genre in event.get("classifications", list())
                    ],
                    event.get("promoter", dict()),
                    [
                        venue
                        for venue in event.get("_embedded", dict()).get(
                            "venues", None
                        )
                    ],
                    [
                        genre.get("externalLinks")
                        for genre in event.get("_embedded", dict()).get(
                            "attractions", None
                        )
                    ],
                )
            )
        return parsed
