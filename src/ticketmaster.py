"""
Calls Ticketmaster API endpoint to get event data in Amsterdam
based on the artist that was collected from Spotify playlist API
and format the data.
"""

import os
import logging
from dotenv import load_dotenv  # pip3 install python-dotenv

# from helpers.api_requests import make_request
from helpers.variables import Artist, Event

load_dotenv()

TICKETMASTER_KEY = os.getenv("TICKETMASTER_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TICKETMASTER")
logger.setLevel(logging.INFO)


class TicketmasterAPI:
    def __init__(self, tracks: list[Artist]):
        """Initialize Ticketmaster API class"""
        self.tracks = tracks
        self.all_events = []
        self.checked_artists = []

    def run(self):
        """Run Ticketmaster API class"""
        for item in self.tracks:
            for artist in item.artists:
                self._find_event(artist)

    def _find_event(self, artist: str):
        """Find event based on artist

        Args:
            artist (str): artist name
        """
        ...
        # if artist in self.checked_artists:
        #     return

        # self.checked_artists.append(artist)

        # city = "Amsterdam"
        # artist = artist.lower().replace(" ", "_").replace("-", "_")

        # url = f"https://app.ticketmaster.com/discovery/v2/events.json?keyword=\
        #         {artist}&city={city}&apikey={TICKETMASTER_KEY}"
        # data = make_request(url, service="ticketmaster")

        # if data and data.get("page", {}).get("totalElements") == 0:
        #     return

        # if data:
        #     self.parse_data(data, artist)

    def parse_data(self, data: dict, artist: str):
        """Clean up data.

        Args:
            data (dict): dictionary that has the data
            artist (str): name of artist
        """
        events = data.get("_embedded", {}).get("events")
        events_of_artist = self.parse_details(events, artist)
        self.all_events.append({"artist": artist, "concerts": events_of_artist})

    def parse_details(self, events: dict, artist: str) -> list[Event]:
        """Gets detailed information on events.

        Args:
            events (dict): combination of events
            artist (str): name of artists

        Returns:
            list: collection of Events
        """
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
                    event.get("dates", {}).get("start", {}).get("localDate", None),
                    event.get("dates", {}).get("start", {}).get("localTime", None),
                    event.get("dates", {}).get("timezone", {}),
                    event.get("dates", {}).get("status", {}).get("code", None),
                    [genre.get("genre") for genre in event.get("classifications", [])],
                    event.get("promoter", {}),
                    [venue for venue in event.get("_embedded", {}).get("venues", None)],
                    [
                        genre.get("externalLinks")
                        for genre in event.get("_embedded", {}).get("attractions", None)
                    ],
                )
            )
        return parsed
