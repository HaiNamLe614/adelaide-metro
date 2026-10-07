# Decisions

## Schema

**Times stored as INTEGER seconds since midnight, not TIME**
GTFS allows values past 24:00:00 (a trip starting 11:40pm might have a
stop at 25:30:00, meaning 1:30am the next service day). Postgres TIME
rejects anything over 23:59:59. Seconds-since-midnight handles this with
no special cases, sorts and compares normally, and indexes well.

**stop_times primary key is (trip_id, stop_sequence)**
Neither column is unique alone. A trip appears once per stop it visits;
a stop appears once per trip that visits it. Together they're unique.

**Day columns are BOOLEAN, not INTEGER**
Lets queries read `WHERE monday` instead of `WHERE monday = 1`.
Cost: the loader has to cast explicitly with astype(bool), because
psycopg2 sends Python ints as typed integers and Postgres refuses
the implicit cast. MySQL would have accepted it silently.

**Dates converted from YYYYMMDD integers to DATE**
Enables real date comparisons like BETWEEN start_date AND end_date.
Conversion happens in the loader via pd.to_datetime(format="%Y%m%d").

## Loading

**Loader truncates before inserting**
Makes the script idempotent — same result whether run once or ten times.
Without it, rerunning hits primary key violations.

**ID columns forced to string with dtype=**
Pandas infers numeric IDs as int64, which breaks joins to text columns
and would strip leading zeros.

## Open

- Database password is hardcoded in load.py. Move to env var before
  this goes on GitHub.

**Index on stop_times (stop_id, departure_secs)**
Measured on 823,126 rows: 0.129 ms with index, 31.110 ms without (241x).
Without it Postgres does a parallel seq scan, examining ~274k rows per
worker to return 9, then sorts. With it, the index satisfies both the
filter and the ORDER BY, so no sort step is needed. Column order matters:
stop_id first (equality), departure_secs second (range + sort).
