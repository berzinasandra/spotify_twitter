"""
Calls Spotify API endpoint to get tracks from playlists
and format the recieve data 
"""

from dotenv import load_dotenv  # pip3 install python-dotenv
import os
import logging
from helpers.api_requests import make_request, get_token
from helpers.utils import list_files, read_file, save_as_parquet
from helpers.variables import Artist
from helpers.variables import SPOTIFY_RAW_DATA_PATH, SPOTIFY_PROCESSED_DATA_PATH
from pandas import DataFrame
import pandas as pd


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SPOTIFY")
logger.setLevel(logging.INFO)

load_dotenv()
SPOTIFY_SHAZAM_PLAYLIST_ID = os.getenv("SPOTIFY_SHAZAM_PLAYLIST_ID")
SPOTIFY_STAR_PLAYLIST_ID = os.getenv("SPOTIFY_STAR_PLAYLIST_ID")


class SpotifyAPI:
    def __init__(self):
        self.playlist_names = [
            {
                "playlist_name": "My Shazam Tracks",
                "endpoint": "https://api.spotify.com/v1/playlists/"
                + SPOTIFY_SHAZAM_PLAYLIST_ID
                + "/tracks?&offset=",
            },
            {
                "playlist_name": "Star",
                "endpoint": "https://api.spotify.com/v1/playlists/"
                + SPOTIFY_STAR_PLAYLIST_ID
                + "/tracks?&offset=",
            },
        ]
        self.all_tracks = []

    
    def run(self):
        for playlist in self.playlist_names:
            self.extract_tracks_from_playlist(playlist)
            
        self.extract_track_details()
        self.parse_details()

    def extract_tracks_from_playlist(self, playlist:dict[str, str]) -> None:
        spotify_token = get_token()
        offset = 0
        songs_in_playlist = True
        while songs_in_playlist:
            url = playlist.get("endpoint", None)
            logger.info(
                f"Collecting songs from playlist"
                f"{playlist.get('playlist_name', None)},"
                f"offset {offset}"
            )
            tracks = make_request(url, offset, "spotify", spotify_token)
            offset += 100
            # songs_in_playlist = True if tracks else False
            songs_in_playlist = False

    def extract_track_details(self) -> None:
        """_summary_
        """
        import pandas as pd
        files = list_files(SPOTIFY_RAW_DATA_PATH)
        for file in files:
            logger.info(f"Start parsing details from file {file}")
            df = read_file(file)
            details_df = self.parse_details(df)
            file_name = file.split('/')[-1].split(".")[0]
            output_path = f"{SPOTIFY_PROCESSED_DATA_PATH}{file_name}.parquet"
            import pdb;pdb.set_trace()
            save_as_parquet(details_df, output_path)





    def parse_details(self, df: DataFrame):
        details: list[Artist] = []
        for row in df.itertuples():
            added_at = row.added_at
            track = row.track
            artists = [artist["name"] for artist in track["artists"]]
            song_title = track.get('name', None)
            album_image= track.get('album', None).get("images")
            release_date = track.get('album', None).get("release_date")
            details.append(Artist(
                added_at,
                artists, 
                song_title,
                album_image,
                release_date,
            ))

        return pd.DataFrame(details)

