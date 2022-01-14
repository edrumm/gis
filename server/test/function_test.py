# Placeholder
import server.database as database
import server.functions as func
from pytest import fail


def text_convex_hull():
    try:
        # Works in Flask as it should, does not work in pytest. Seems to be no solution... WHY?
        # "psycopg2.OperationalError: connection to server at "localhost" (::1),
        # port 5432 failed: fe_sendauth: no password supplied"
        #
        # TODO: Swap params for .env values (if solution found to above problem...)
        db = database.Database('localhost', 'nyc', '<username removed for security>', '<password removed for security>')

        geom = func.convex_hull(db, 'geom', 'nyc_subway_stations')

        assert not geom.is_empty

    except Exception as err:
        fail(err)


def test_count_points_in_polygon():
    pass


def test_slope():
    pass


def test_viewshed():
    pass
