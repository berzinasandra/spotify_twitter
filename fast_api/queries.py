import pandas as pd
from pandas import DataFrame
from src.helpers.variables import SPOTIFY_PROCESSED_DATA_PATH
from src.helpers.utils import list_files
from typing import Optional, Union, TypedDict

# TODO: load data in DB
# TODO: read data from DB 


class ArtistSongs(TypedDict):
    artist: str
    songs: list

def _read_all_files() -> DataFrame:
    """Gathers all details in Spotify Processed directory into one DataFrame

    Returns:
        DataFrame: all song details in DataFrame
    """
    files = list_files(SPOTIFY_PROCESSED_DATA_PATH)
    all_dfs : list = list()
    for file in files:
        df = pd.read_parquet(file)
        all_dfs.append(df)    
    main_df = pd.concat(all_dfs)
    return main_df


def retrieve_all_artists() -> list:
    """Gets a list of all main artists who's record(s) is collected from Spotify

    Returns:
        list: list of all artists
    """
    df = _read_all_files
    # TODO: maybe parallel processing
    artists = df['main_artist'].unique().tolist()
    return artists
    
def retrieve_all_songs_from_artist(artist:str) -> Union[ArtistSongs, list[ArtistSongs]]:
    """Return artist and it's songs.
    If given only part of Artist name finds all artists with given phrase/character and returns all artists and their songs

    Args:
        artist (str): Artis name or part of it

    Returns:
        Union[ArtistSongs, list[ArtistSongs]]: artist and their songs 
    """

    df = _read_all_files()
    artist = artist.title()
    artist_df = df[df["main_artist"] == artist]
    if artist_df.empty:
        # TODO: try to find closest match 
        artist_df = df[df["main_artist"].str.contains(artist)]
        if artist_df.empty:
            return f"No such artist - {artist } found"
        
        artists = artist_df["main_artist"].unique().tolist()
        collection:list = list()
        for unique_artist in artists:
            songs = artist_df[artist_df["main_artist"] == unique_artist]["song_title"].tolist()
            collection.append({unique_artist:songs})
        return collection
        
    songs = artist_df["song_title"].unique().tolist()
    return {artist: songs}


def retrieve_details_based_on_date(date):
    ...
    # TODO: 
    # format date in right format, if not possible error out
    # chekck if date in past ??

