import enum

from fastapi import FastAPI, HTTPException

from fast_api.queries import (
    retrieve_all_artists,
    retrieve_all_songs_from_artist,
    retrieve_details_based_on_dates,
)

DATE_FORMAT = "YYYY-MM-DD"


class DateType(enum):
    ADDED_AT = "added_at"
    RELEASE_DATE = "release_date"


app = FastAPI()


@app.get("/artists/")
def get_all_artists():
    return {"all_artists": retrieve_all_artists()}


@app.get("/artists/{artist}")
def get_songs_from_given_artist(artist):
    return retrieve_all_songs_from_artist(artist)


@app.get("/dates/")
def get_tracks_based_on_dates(start: str, end: str, date_type: str):
    def _valid_dates(start: str, end: str) -> bool:
        import datetime

        try:
            start_result, end_result = (
                bool(datetime.strptime(start, DATE_FORMAT)),
                bool(datetime.strptime(end, DATE_FORMAT)),
            )
        except ValueError:
            start_result, end_result = False, False
        return start_result, end_result

    if not _valid_dates(start, end):
        HTTPException(
            status_code=404,
            detail=f"Invalid start and/or end date: start date - {start}, end date - {end}",
        )

    if date_type in [DateType.ADDED_AT, DateType.RELEASE_DATE]:
        HTTPException(
            status_code=404,
            detail=f"Invalid date type, excepted {DateType.ADDED_AT} or {DateType.RELEASE_DATE}",
        )

    details = retrieve_details_based_on_dates(start, end, date_type)
    return {date_type: details}
