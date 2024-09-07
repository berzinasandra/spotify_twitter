from fastapi import FastAPI
from pydantic import BaseModel
from fast_api.queries import retrieve_all_artists, retrieve_all_songs_from_artist, retrieve_details_based_on_date

app = FastAPI()


@app.get("/artists/")
def get_all_artists():
    return {"all_artists": retrieve_all_artists()}



@app.get("/artists/{artist}")
def get_all_artists(artist):
    return retrieve_all_songs_from_artist(artist)


@app.get("/artists/{date}")
def get_all_artists(date):
    # Needed format is YYYY-MM-DD
    return retrieve_details_based_on_date(date)