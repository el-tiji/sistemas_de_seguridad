from sqlalchemy import create_engine, text
import os

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    existe = conn.execute(
        text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'usuario'
        )
        """)
    ).scalar()

    if not existe:
        with open("src/backend/db/database.sql") as f:
            sql = f.read()

        raw_conn = engine.raw_connection()
        cursor = raw_conn.cursor()
        cursor.execute(sql)
        raw_conn.commit()