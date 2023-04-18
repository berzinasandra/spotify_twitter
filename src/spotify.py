"""
Calls Spotify API endpoint to get tracks from playlists
and format the recieve data 
"""

from dotenv import load_dotenv  # pip3 install python-dotenv
import os
import logging
from helpers.common_functions import make_request
from helpers.common_functions import Artist
from helpers.generate_token import get_token

# TO GET TOKEN NEW 
# https://developer.spotify.com/console/get-artist-albums/?id=&include_groups=&market=&limit=&offset=

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
        spotify_token = get_token()
        for playlist in self.playlist_names:
            offset = 0
            songs_in_playlist = True
            while songs_in_playlist:
                url = playlist.get("endpoint", None)
                logger.info(
                    f"Collecting songs from playlist \
                    {playlist.get('playlist_name', None)}, \
                    offset {offset}"
                )
                tracks = make_request(url, offset, "spotify", spotify_token)
                offset += 100
                songs_in_playlist = True if tracks else False
                if songs_in_playlist:
                    self.parse_details(tracks)

        return self.all_tracks

    def parse_details(self, items: dict):
        for item in items:
            if not item:
                continue
            self.all_tracks.append(
                Artist(
                    item.get("added_at", None),
                    [
                        artist["name"]
                        for artist in item.get("track", dict()).get("artists", list())
                    ],
                    item.get("track", dict()).get("name", None),
                    item.get("track", dict()).get("album", dict()).get("images"),
                    item.get("track", dict()).get("album", dict()).get("release_date"),
                )
            )
