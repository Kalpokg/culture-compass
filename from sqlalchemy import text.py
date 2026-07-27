from sqlalchemy import text
from culture_compass.database.session import engine  # however you create your engine

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE events RESTART IDENTITY CASCADE"))
    conn.execute(text("TRUNCATE TABLE venues RESTART IDENTITY CASCADE"))
    conn.execute(text("TRUNCATE TABLE cities RESTART IDENTITY CASCADE"))
    conn.execute(text("TRUNCATE TABLE countries RESTART IDENTITY CASCADE"))
    conn.execute(text("TRUNCATE TABLE sources RESTART IDENTITY CASCADE"))