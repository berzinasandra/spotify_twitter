from typing import TypedDict, Union

from fast_api.common import read_all_files
from src.helpers.spotify.variables import SPOTIFY_PROCESSED_DATA_PATH

# TODO: load data in DB
# TODO: read data from DB


class ArtistSongs(TypedDict):
    artist: str
    songs: list


def retrieve_all_artists() -> list[str]:
    """Gets a list of all main artists who's record(s) is collected from Spotify

    Returns:
        list: list of all artists
    """
    df = read_all_files(SPOTIFY_PROCESSED_DATA_PATH)
    artists = df["main_artist"].unique().tolist()
    return artists


def retrieve_all_songs_from_artist(
    artist: str,
) -> Union[ArtistSongs, list[ArtistSongs]]:
    """Return artist and it's songs.
    If given only part of Artist name finds all artists
    with given phrase/character and returns all artists and their songs

    Args:
        artist (str): Artist name or part of it

    Returns:
        Union[ArtistSongs, list[ArtistSongs]]: artist and their songs
    """

    df = read_all_files(SPOTIFY_PROCESSED_DATA_PATH)
    artist = artist.title()
    artist_df = df[df["main_artist"] == artist]
    if artist_df.empty:
        artist_df = df[df["main_artist"].str.contains(artist)]
        if artist_df.empty:
            return f"No such artist - {artist } found"

        artists = artist_df["main_artist"].unique().tolist()
        collection: list = []
        for unique_artist in artists:
            songs = artist_df[artist_df["main_artist"] == unique_artist][
                "song_title"
            ].tolist()
            collection.append({unique_artist: songs})
        return collection

    songs = artist_df["song_title"].unique().tolist()
    return {artist: songs}


def retrieve_details_based_on_dates(
    start: str, end: str, date_type: str
) -> list[dict[str, str]]:
    """Retrieves song details based on given start
    and end date for either release date or added_at date

    Args:
        start (str): start date
        end (str): end date
        date_type (str): release date or added_at date

    Returns:
        list: list of songs and artist name
    """
    df = read_all_files(SPOTIFY_PROCESSED_DATA_PATH)

    specified_timeframe_df = df[(df[date_type] >= start) & (df[date_type] <= end)]

    if specified_timeframe_df:
        return f"No data found with start date {start}, end date {end} for date type {date_type}"
    result = (
        specified_timeframe_df[["main_artist", "song_title", date_type]]
        .apply(lambda x: x.to_dict(), axis=1)
        .to_list()
    )
    return result
