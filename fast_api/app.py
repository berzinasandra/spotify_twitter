from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/artists/")
def get_all_artists():
    # Read file
    