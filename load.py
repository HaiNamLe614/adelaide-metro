import pandas as pd
from sqlalchemy import create_engine, text

def to_secs(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

engine = create_engine("postgresql+psycopg2://postgres:dev@localhost:5432/metro")
with engine.begin() as conn:
    conn.execute(text("TRUNCATE stop_times, trips, calendar, routes, stops CASCADE"))

stops = pd.read_csv("data/stops.txt", dtype={"stop_id": str, "stop_code": str})
stops = stops[["stop_id", "stop_name", "stop_lat", "stop_lon"]]
stops.to_sql("stops", engine, if_exists="append", index=False)

routes = pd.read_csv("data/routes.txt", dtype={"route_id": str})
routes = routes[["route_id", "route_short_name", "route_long_name", "route_type"]]
routes.to_sql("routes", engine, if_exists="append", index=False)

cal = pd.read_csv("data/calendar.txt", dtype={"service_id": str})
cal = cal[["service_id", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "start_date", "end_date"]]
cal["start_date"] = pd.to_datetime(cal["start_date"], format="%Y%m%d")
cal["end_date"] = pd.to_datetime(cal["end_date"], format="%Y%m%d")
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
cal[days] = cal[days].astype(bool)
cal.to_sql("calendar", engine, if_exists="append", index=False)

trips = pd.read_csv("data/trips.txt", dtype={"route_id": str, "service_id": str, "trip_id": str})
trips = trips[["route_id", "service_id", "trip_id"]]
trips.to_sql("trips", engine, if_exists="append", index=False)

stop_times = pd.read_csv("data/stop_times.txt", dtype={"trip_id": str, "stop_id": str})
stop_times["arrival_secs"] = stop_times["arrival_time"].map(to_secs)
stop_times["departure_secs"] = stop_times["departure_time"].map(to_secs)
stop_times = stop_times[["trip_id", "arrival_secs", "departure_secs", "stop_id", "stop_sequence"]]
stop_times.to_sql("stop_times", engine, if_exists="append", index=False)

print(f"loaded {len(stops)} rows into the stops table")
print(f"loaded {len(routes)} rows into the routes table")   
print(f"loaded {len(trips)} rows into the trips table")
print(f"loaded {len(cal)} rows into the calendar table")   
print(f"loaded {len(stop_times)} rows into the stop_times table")