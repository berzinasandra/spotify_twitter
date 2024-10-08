from typing import NamedTuple

SCHEMA_VERSION = "0.0"
TICKETMASTER_RAW_DATA_PATH = "data/ticketmaster/raw"
TICKETMASTER_RAW_FILENAME = "ticketmaster_raw.parquet"
TICKETMASTER_PROCESSED_DATA_PATH = f"data/ticketmaster/processed/{SCHEMA_VERSION}v/"

CITY = "amsterdam"
TICKETMASTER_API_URL = "https://app.ticketmaster.com/discovery/v2/events.json?keyword="


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
