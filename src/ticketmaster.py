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
)
from helpers.ticketmaster.api_requests import request_ticketmaster_endpoint
from helpers.utils import list_files, save_as_parquet
import pandas as pd
from helpers.spotify.variables import SPOTIFY_PROCESSED_DATA_PATH
from time import sleep

load_dotenv()


TICKETMASTER_KEY = os.getenv("TICKETMASTER_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TICKETMASTER")


class TicketmasterAPI:
    def __init__(self):
        self.artists: list = []
        self.all_events = []
        self.checked_artists = []
        self.raw_events = []

    def run(self):
        """Executes Ticketmaster API class.
        1. Reads all processed files from spotify
        2. Gets unique artists TODO: save unique artists soemwhere else.
        3. Query Ticketmaster API
        4. Save results (for now locally) TODO: upgrade this
        5. Process results
        """
        files = list_files(SPOTIFY_PROCESSED_DATA_PATH)
        self._collect_unique_artists(files)

        for artist in self.artists:
            sleep(5)
            self._retrieve_event(artist)
        df = pd.DataFrame(self.raw_events)
        # import pdb;pdb.set_trace()
        save_as_parquet(df, TICKETMASTER_RAW_DATA_PATH + TICKETMASTER_RAW_FILENAME)
        self.parse_data()

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

    def _retrieve_event(self, artist: str):
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
        data = request_ticketmaster_endpoint(url)

        # if data and data.get("page", dict()).get("totalElements") == 0:
        #     # TODO: no concert for artist
        #     return
        self.raw_events.append(data)

        # import pdb;pdb.set_trace()

    def parse_data(self):
        df = pd.read_parquet(TICKETMASTER_RAW_DATA_PATH + TICKETMASTER_RAW_FILENAME)
        print(df)
        import pdb

        pdb.set_trace()

        # events = data.get("_embedded", dict()).get("events")
        # events_of_artist = self.parse_events(events, artist)
        # self.all_events.append({"artist": artist, "concerts": events_of_artist})

    def parse_events(self, events: dict, artist: str):
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
                        for venue in event.get("_embedded", dict()).get("venues", None)
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
