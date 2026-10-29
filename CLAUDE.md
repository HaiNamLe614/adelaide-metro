# Metro GTFS Project

Portfolio project. I'm a CS graduate filling gaps in production engineering
(Postgres, FastAPI, Docker, AWS) before applying for backend and ML roles.
The point is that I understand the code, not that it ships fast.

## Rules
- Do NOT write SQL queries, schema, or core business logic. Explain the
  options and the tradeoffs, then let me write it.
- Boilerplate is fine: Dockerfiles, CI configs, test scaffolding, imports.
- When I ask why something works, explain it rather than just fixing it.
- Before suggesting a library or pattern, say what the alternative is.
- Don't build ahead of the current week in the plan below.

## Stack
Postgres 16 in Docker, Python 3.14, SQLAlchemy async with asyncpg, FastAPI,
pandas. Data is Adelaide Metro GTFS: 823k stop times, 22k trips, 9k stops.

## Where this is going
A transit query API, deployed publicly, with an LLM layer added last. The
design point I want to demonstrate is that most timetable questions are SQL,
not semantic search, so the LLM routes queries rather than answering them.
Not building a frontend.

## Plan
- Week 1: schema + loader — done
- Week 2: async FastAPI + Pydantic — current
- Week 3: Docker + docker-compose
- Week 4: AWS deployment (ECS, RDS, one Lambda), live URL
- Week 5: scheduled pipeline for the GTFS realtime feed
- Week 6: pytest with a test database, GitHub Actions CI/CD, structured
  logging, and a postmortem from deliberately breaking production
- Week 7: LLM query routing + RAG over service alerts

## Testing
Manual curl for now. Real tests are week 6, pytest against a throwaway
Postgres container. Don't add a test suite before then.

## Known gaps, in priority order
1. load.py drops trip_headsign and direction_id — fixing now
2. idx_stop_times_stop_dep is in the live DB but not in schema.sql
3. departures query ignores calendar start_date/end_date, and
   calendar_dates.txt (1,130 holiday exception rows) is not loaded at all.
   This is a correctness bug: the API currently claims buses run on public
   holidays. Fixing after the two above.
4. departure_secs is returned raw; needs formatting to a readable time

## Context
DECISIONS.md has the design decisions made so far and why. Append to it when
a decision has a real alternative worth recording.