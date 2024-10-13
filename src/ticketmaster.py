"""
Calls Ticketmaster API endpoint to get event data in Amsterdam
based on the artist that was collected from Spotify playlist API
and format the data.
"""

import os
import logging
from dotenv import load_dotenv  # pip3 install python-dotenv
from helpers.ticketmaster.variables import (
    CITY,
    TICKETMASTER_API_URL,
    Event,
    TICKETMASTER_RAW_DATA_PATH,
    TICKETMASTER_RAW_FILENAME,
    TICKETMASTER_PROCESSED_DATA_PATH,
    TICKETMASTER_PROCESSED_FILENAME,
)
from helpers.ticketmaster.api_requests import request_ticketmaster_endpoint
from helpers.utils import save_as_parquet
import pandas as pd
from requests import Session
from typing import Collection

load_dotenv()


TICKETMASTER_KEY = os.getenv("TICKETMASTER_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TICKETMASTER")


class TicketmasterAPI:
    def __init__(self):
        self.artists: list = []
        self.all_events: list[dict[str, Collection[Event]]] = []
        self.checked_artists = []
        self.raw_events = []

    def run(self):
        """Executes Ticketmaster API class.
        1. Reads all processed files from spotify
        2. Gets unique artists TODO: save unique artists soemwhere else.
        3. Query Ticketmaster API
        4. Save results (for now locally) TODO: upgrade this
        5. Process results & save locally
        """
        # files = list_files(SPOTIFY_PROCESSED_DATA_PATH)
        # self._collect_unique_artists(files)
        # session = create_session()
        # for i, artist in enumerate(self.artists, start=1):
        #     logger.info(f"Starting to search for artist {i}/{len(self.artists)}...")
        #     self._retrieve_event(artist, session)
        # df = pd.DataFrame(self.raw_events)
        # save_as_parquet(df, TICKETMASTER_RAW_DATA_PATH + TICKETMASTER_RAW_FILENAME)
        self.parse_data()
        import pdb

        pdb.set_trace()
        df = pd.DataFrame(self.all_events)
        save_as_parquet(
            df, TICKETMASTER_PROCESSED_DATA_PATH + TICKETMASTER_PROCESSED_FILENAME
        )

    def _collect_unique_artists(self, files: list):
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

    def _retrieve_event(self, artist: str, session: Session):
        """_summary_

        Args:
            artist (str): _description_
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

    def parse_data(self):
        df = pd.read_parquet(
            TICKETMASTER_RAW_DATA_PATH + "/" + TICKETMASTER_RAW_FILENAME
        )
        for name, column in df.iterrows():
            artist_field = column["_links"].get("self", dict()).get("href")
            artist = artist_field.split("=")[-1].replace("_", " ")
            if not column["_embedded"]:
                logger.info(f"No events found for {artist.title()}")
                continue

            events = column.get("_embedded", dict()).get("events")
            artist_events = self.parse_events(events, artist)
            self.all_events.append({"artist": artist, "concerts": artist_events})

    def parse_events(self, events: dict, artist):
        parsed = []
        logger.info(f"Found events for artist {artist.title()}")
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
                    [
                        venue
                        for venue in event.get("_embedded", dict()).get("venues", None)
                    ],
                )
            )
        return parsed
