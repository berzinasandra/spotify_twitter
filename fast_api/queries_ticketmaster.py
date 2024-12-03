import re
from typing import TypedDict, Union

from fast_api.common import read_all_files
from src.helpers.ticketmaster.variables import TICKETMASTER_PROCESSED_DATA_PATH

# TODO: load data in DB
# TODO: read data from DB


class ArtistEvents(TypedDict):
    artist: str
    events: list


def retrieve_all_events() -> list[str]:
    """Gets a list of all artists who's events are collected from Ticketmaster

    Returns:
        list: list of all artists
    """
    df = read_all_files(TICKETMASTER_PROCESSED_DATA_PATH)
    print(df.columns)
    artist_events = df["artist"].unique().tolist()
    return artist_events


def _clean_event_name(event_names: list[str]) -> list[str]:
    """Clean event names

    Args:
        event_names given event names

    Returns:
        list[str]: return only event names that don't consist of given features
    """
    dirty_event_name_features = ["VIP", r"\|"]
    return list(
        set(
            [
                event
                for event in event_names
                for feature in dirty_event_name_features
                if not re.search(feature, event)
            ]
        )
    )


def retrieve_all_events_from_artist(
    artist: str,
) -> Union[ArtistEvents, list[ArtistEvents]]:
    """Return events based on given artists.
    If given only part of Artist name finds all artists
    with given phrase/character and returns all artists and their events

    Args:
        artist (str): Artist name or part of it

    Returns:
        Union[ArtistEvents, list[ArtistEvents]]: artist and their songs
    """

    df = read_all_files(TICKETMASTER_PROCESSED_DATA_PATH)
    artist_df = df[df["artist"] == artist]
    if artist_df.empty:
        artist_df = df[df["artist"].str.contains(artist)]
        if artist_df.empty:
            return f"No such artist - {artist } found"

        artists = artist_df["artist"].unique().tolist()
        collection: list = []
        for unique_artist in artists:
            events = artist_df[artist_df["artist"] == unique_artist][
                "event_name"
            ].tolist()
            events = _clean_event_name(events)
            collection.append({unique_artist: events})
        return collection

    events = artist_df["event_name"].unique().tolist()
    events = _clean_event_name(events)
    return {artist: events}
