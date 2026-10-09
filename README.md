# Adelaide Metro Transit Data

Postgres schema and loader for Adelaide Metro GTFS data: 823k stop times,
22k trips, 9k stops.

## Setup

```bash
docker run --name metro-db -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=metro -p 5432:5432 -d postgres:16
docker exec -i metro-db psql -U postgres -d metro < schema.sql
python load.py
```

## Design notes

Times are stored as seconds since midnight rather than Postgres TIME.
GTFS allows values past 24:00:00 for trips crossing midnight, which TIME
rejects.

The composite index on (stop_id, departure_secs) takes the next-departures
query from 31.1ms to 0.129ms. It also removes the sort step, since the
index already returns rows in departure order.

Full reasoning in DECISIONS.md.

## Data

Adelaide Metro GTFS feed, Department for Infrastructure and Transport,
CC-BY licensed.
