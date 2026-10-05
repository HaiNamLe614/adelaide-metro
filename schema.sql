CREATE TABLE stops (
    stop_id   TEXT PRIMARY KEY,
    stop_code TEXT,
    stop_name TEXT NOT NULL,
    stop_lat  DOUBLE PRECISION,
    stop_lon  DOUBLE PRECISION
);

CREATE TABLE routes (
    route_id         TEXT PRIMARY KEY,
    route_short_name TEXT,
    route_long_name  TEXT,
    route_type       INTEGER
);

CREATE TABLE calendar (
    service_id TEXT PRIMARY KEY,
    monday     BOOLEAN,
    tuesday    BOOLEAN,
    wednesday  BOOLEAN,
    thursday   BOOLEAN,
    friday     BOOLEAN,
    saturday   BOOLEAN,
    sunday     BOOLEAN,
    start_date DATE,
    end_date   DATE
);

CREATE TABLE trips (
    trip_id       TEXT PRIMARY KEY,
    route_id      TEXT NOT NULL REFERENCES routes(route_id),
    service_id    TEXT NOT NULL REFERENCES calendar(service_id),
    trip_headsign TEXT,
    direction_id  INTEGER
);

CREATE TABLE stop_times (
    trip_id        TEXT NOT NULL REFERENCES trips(trip_id),
    stop_sequence  INTEGER NOT NULL,
    stop_id        TEXT NOT NULL REFERENCES stops(stop_id),
    arrival_secs   INTEGER NOT NULL,
    departure_secs INTEGER NOT NULL,
    PRIMARY KEY (trip_id, stop_sequence)
);

CREATE INDEX idx_stop_times_stop_dep ON stop_times (stop_id, departure_secs);
