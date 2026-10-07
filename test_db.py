from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://postgres:dev@localhost:5432/metro")

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM stops"))
    print(result.scalar())