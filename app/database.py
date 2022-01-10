import psycopg2 as pg
from flask import Blueprint


postgres = Blueprint('postgres', __name__)


def test():
    return 'Hello!'


def connect():
    # Read credentials from .env
    conn = pg.connect('')
    cur = conn.cursor()

    return conn, cur
