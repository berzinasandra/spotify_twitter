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


class Event(NamedTuple):
    """
    Formatting data for detected events
    """

    ticket_type_name: str
    ticket_type_id: str
    ticket_url: list
    concert_date: str
    concert_starting_time: str
    concert_timezone: str
    tikcet_status: str
    genre: list
    promoter_info: dict
    venues: list
    social_media_links: list
