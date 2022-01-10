import psycopg2 as pg
from dotenv import dotenv_values


def connect():
    config = dotenv_values('.env')

    pg_user = config.get('PG_USER')
    pg_host = config.get('PG_HOST')
    pg_password = config.get('PG_PASSWORD')
    pg_db = config.get('PG_DB')

    conn = pg.connect(host=pg_host, database=pg_db, user=pg_user, password=pg_password)
    cur = conn.cursor()

    return conn, cur
