import http.client
import os
import psycopg2
import atexit
from dotenv import load_dotenv
from controllers.athletecontroller import AthleteController
from controllers.segmentcontroller import get_athlete_segment_efforts

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
    athlete_controller.get_all_user_year_activities()

    for athlete in athlete_controller.get_all_athletes():
        firstname = athlete[0]
        lastname = athlete[1]
        refresh_token = athlete[2]

        get_athlete_segment_efforts(firstname, lastname, refresh_token)

atexit.register(close_connection, connection)
