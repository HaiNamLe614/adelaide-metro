import os
from fastapi import FastAPI, HTTPException
from models import Departure
from db import engine
from sqlalchemy import text

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/stops/{stop_id}/departures", response_model=list[Departure])
async def get_departures(stop_id: str, after: int = 50400, day: str = "monday"):
    async with engine.connect() as conn:
        VALID_DAYS = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
        if day not in VALID_DAYS:
            raise HTTPException(status_code=400, detail=f"Invalid day: {day}. Must be one of {VALID_DAYS}")
        result = await conn.execute(
            text(f"""
            SELECT r.route_short_name, t.trip_headsign, st.departure_secs
            FROM stop_times st
            JOIN trips t    ON st.trip_id = t.trip_id
            JOIN routes r   ON t.route_id = r.route_id
            JOIN calendar c ON t.service_id = c.service_id
            WHERE st.stop_id = :stop_id
            AND st.departure_secs > :after
            AND c.{day}
            ORDER BY st.departure_secs
            LIMIT 10
            """),
            {"stop_id": stop_id, "after": after, "day": day}
        )
        rows = result.fetchall()
    return [
        Departure(
            route=row.route_short_name,
            headsign=row.trip_headsign,
            departure_time=str(row.departure_secs)
        )
        for row in rows
    ]