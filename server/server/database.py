import psycopg2 as pg


def test():
    return 'Hello!'


def connect():
    # Read credentials from .env
    conn = pg.connect('')
    cur = conn.cursor()

    return conn, cur
