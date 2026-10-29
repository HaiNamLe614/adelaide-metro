from pydantic import BaseModel

class Departure(BaseModel):
    route: str
    headsign: str | None
    departure_time: str