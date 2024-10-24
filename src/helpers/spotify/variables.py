from datetime import datetime
from typing import NamedTuple

SCHEMA_VERSION = "0.0"
SPOTIFY_RAW_DATA_PATH = "data/spotify/raw"
SPOTIFY_PROCESSED_DATA_PATH = f"data/spotify/processed/{SCHEMA_VERSION}v/"
TICKETMASTER_RAW_DATA_PATH = "data/ticket_master/raw"


class Artist(NamedTuple):
    """
    Formatting data for artists
    """

    added_at: datetime
    main_artist: str
    artists: list
    song_title: dict
    images: list
    release_date: str
