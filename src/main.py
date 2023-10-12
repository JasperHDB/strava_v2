import http.client
import os
import psycopg2
import atexit
from dotenv import load_dotenv
from controllers.athletecontroller import AthleteController
from controllers.athletecontroller import get_access_token

stravahttpconnection = http.client.HTTPSConnection("www.strava.com")

load_dotenv('../.env')

try:
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"))
except psycopg2.Error as e:
    print("Error connecting to the database:", e)
    exit()

athlete_controller = AthleteController(connection)


def close_connection(conn):
    """
    Close the active connection

    Args:
        conn (_T_conn): The active connection
    """
    if conn:
        conn.close()


if __name__ == "__main__":
    # get_all_user_year_activities()

    print(get_access_token(athlete_controller.get_refresh_token(15376382)))

atexit.register(close_connection, connection)
