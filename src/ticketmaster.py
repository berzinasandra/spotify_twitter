import logging
from typing import Collection

import pandas as pd
from requests import Session

from constants import TICKETMASTER_KEY
from helpers.spotify.variables import SPOTIFY_PROCESSED_DATA_PATH
from helpers.ticketmaster.api_requests import request_ticketmaster_endpoint
from helpers.ticketmaster.variables import (
    CITY,
    TICKETMASTER_API_URL,
    TICKETMASTER_PROCESSED_DATA_PATH,
    TICKETMASTER_PROCESSED_FILENAME,
    TICKETMASTER_RAW_DATA_PATH,
    TICKETMASTER_RAW_FILENAME,
    Event,
)
from helpers.utils import create_session, list_files, save_as_parquet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TICKETMASTER")


class TicketmasterAPI:
    """Calls Ticketmaster API endpoint to get event data in Amsterdam
    based on the artist that was collected from Spotify playlist API
    and format the data.
    """

    def __init__(self):
        self.artists: list = []
        self.all_events: list[dict[str, Collection[Event]]] = []
        self.checked_artists = []
        self.raw_events = []

    def run(self):
        """Executes Ticketmaster API class.
        1. Reads all processed files from spotify
        2. Gets unique artists TODO: save unique artists somewhere else.
        3. Query Ticketmaster API
        4. Save results (for now locally) TODO: upgrade this
        5. Process results & save locally
        """
        files = list_files(SPOTIFY_PROCESSED_DATA_PATH)
        self._collect_unique_artists(files)
        session = create_session()
        for i, artist in enumerate(self.artists, start=1):
            logger.info(f"Starting to search for artist {i}/{len(self.artists)}...")
            self._retrieve_event(artist, session)
        df = pd.DataFrame(self.raw_events)
        save_as_parquet(df, TICKETMASTER_RAW_DATA_PATH + TICKETMASTER_RAW_FILENAME)
        self.parse_data()

        df = pd.DataFrame(self.all_events)
        save_as_parquet(
            df, TICKETMASTER_PROCESSED_DATA_PATH + TICKETMASTER_PROCESSED_FILENAME
        )

    def _collect_unique_artists(self, files: list) -> None:
        """Goes over all files with data collected from Spotify and retrieves unique artists

        Args:
            files (list): list of files with data collected from spotify API
        """
        for file in files:
            logger.info(f"Reading {file} and collecting unique artists")
            df = pd.read_parquet(file)
            self.artists.extend(df["main_artist"].unique().tolist())
        self.artists = set(self.artists)
        logger.info(f"Collected {len(self.artists)} unique artists")

    def _retrieve_event(self, artist: str, session: Session) -> None:
        """Using Ticketmaster APi, based on artist and city searches for any event information.

        Args:
            artist (str): name of the artist
        """
        if artist in self.checked_artists:
            return

        self.checked_artists.append(artist)

        # Can't have whitespaces in artist name
        artist = artist.lower().replace(" ", "_").replace("-", "_")
        url = f"{TICKETMASTER_API_URL}{artist}&city={CITY}&apikey={TICKETMASTER_KEY}"

        logger.info(f"Looking for events for artist {artist} - {url}")
        data = request_ticketmaster_endpoint(url, session)
        self.raw_events.append(data)

    def parse_data(self) -> None:
        """
        Reads file with raw data from ticketmaster API and checks if there are any events
        collected for artist. If any, collected data is passed for detail parsing
        """
        df = pd.read_parquet(
            TICKETMASTER_RAW_DATA_PATH + "/" + TICKETMASTER_RAW_FILENAME
        )
        for _, column in df.iterrows():
            artist_field = column["_links"].get("self", {}).get("href")
            artist = artist_field.split("=")[-1].replace("_", " ")
            if not column["_embedded"]:
                logger.info(f"No events found for {artist.title()}")
                continue

            events = column.get("_embedded", {}).get("events")
            self.parse_events(events, artist)

    def parse_events(self, events: dict, artist: str) -> None:
        """Parse details from events

        Args:
            events (dict): dict of all collected events for given artist
            artist (str): artist name
        """
        logger.info(f"Found events for artist {artist.title()}")
        for event in events:
            event_details = dict(
                event_name=event.get("name", None),
                event_id=event.get("id", None),
                event_url=event.get("url", None),
                event_date=event.get("dates", {})
                .get("start", {})
                .get("localDate", None),
                event_time=event.get("dates", {})
                .get("start", {})
                .get("localTime", None),
                event_timezone=event.get("dates", {}).get("timezone", {}),
                event_genre=[
                    genre.get("genre") for genre in event.get("classifications", [])
                ],
                event_venue=list(
                    venue for venue in event.get("_embedded", {}).get("venues", None)
                ),
            )

            self.all_events.append({"artist": artist, **event_details})
