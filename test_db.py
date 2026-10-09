from sqlalchemy import create_engine, text
import os

engine = create_engine(os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:dev@localhost:5432/metro"))

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM stops"))
    print(result.scalar())