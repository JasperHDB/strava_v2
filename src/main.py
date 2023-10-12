import http.client
import json
import os
import psycopg2
import config
import atexit
from time import sleep
from dotenv import load_dotenv
from models.activity import Activity

stravaconnection = http.client.HTTPSConnection("www.strava.com")

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


def get_all_athletes():
    with connection:
        with connection.cursor() as cursor:
            query = ("SELECT firstname, lastname, refresh_token FROM {}.{}"
                     .format(os.getenv("DB_SCHEMA"), os.getenv("DB_TABLE")))
            cursor.execute(query)
            rows = cursor.fetchall()

    if len(rows) == 0:
        print(f"No users were found")

    return rows


def get_access_token(refresh_token):
    """
        Retrieve the access token by trading a refresh token

        Args:
            refresh_token (str): The refresh token of the Strava athlete.

        Returns:
            str: The access token associated with the athlete.

        Raises:
            ValueError: If refresh_token is not passed or wrongly passed
        """
    if not refresh_token:
        raise Exception(f"No refresh token was provided")

    stravaconnection.request("POST",
                             f"/api/v3/oauth/token?client_id={os.getenv('CLIENTID')}"
                             f"&client_secret={os.getenv('CLIENTSECRET')}"
                             f"&grant_type=refresh_token"
                             f"&refresh_token={refresh_token}")

    response = stravaconnection.getresponse().read()
    data = json.loads(response)

    return data['access_token']


def get_refresh_token(athlete_id):
    """
    Retrieve the refresh token associated with a Strava athlete by their ID.

    Args:
        athlete_id (int): The unique identifier of the Strava athlete.

    Returns:
        str: The refresh token associated with the athlete.

    Raises:
        Exception: If no results are found for the given athlete ID in the database.
        ValueError: If athlete_id is not passed or wrongly passed
    """
    if not athlete_id:
        raise ValueError(f"No athlete ID was provided.")

    with connection:
        with connection.cursor() as cursor:
            query = ("SELECT refresh_token FROM {}.{} WHERE strava_athlete_id = %s"
                     .format(os.getenv("DB_SCHEMA"), os.getenv("DB_TABLE")))
            cursor.execute(query, (athlete_id,))
            result = cursor.fetchone()

    if result is None:
        raise Exception(f"No results found for Athlete with ID {athlete_id}")

    return result[0]


def get_data(access_token, call):
    if not call or not access_token:
        return print("Invalid arguments")

    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    stravaconnection.request("GET", call, headers=headers)

    return json.loads(stravaconnection.getresponse().read())


def get_user_year_activities(firstname, lastname, refresh_token):
    if not refresh_token or not firstname or not lastname:
        return ValueError("Invalid arguments")
    if config.activity_limit > 200:
        return ValueError("config.activity_limit cannot exceed 200")
    if not isinstance(config.low_epoch, int) or not isinstance(config.high_epoch, int):
        return ValueError("low_epoch and high_epoch should be integers")
    if config.low_epoch > config.high_epoch:
        return ValueError("low_epoch should be before high_epoch")

    print(f"\nGetting activities of {firstname} {lastname}")

    access_token = get_access_token(refresh_token)

    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    page = 1
    fetched_data = []

    # Iteration for pagination with API
    while True:
        stravaconnection.request("GET",
                                 f"/api/v3/athlete/activities?after={config.low_epoch}"
                                 f"&before={config.high_epoch}"
                                 f"&page={page}"
                                 f"&per_page={config.activity_limit}",
                                 headers=headers)

        raw_activities = json.loads(stravaconnection.getresponse().read())

        if len(raw_activities) == 0:
            break

        fetched_data.extend(raw_activities)
        page += 1

    # If not activities found, skip
    if len(fetched_data) == 0:
        print("No activities found, skipping")
        return

    print(f"Activities found: {len(fetched_data)}")

    activities = []

    # Cleaning up activities
    for raw_activity in fetched_data:
        fullname = ((firstname + " " + lastname)
                    .replace(',', '')
                    .replace('\n', '')
                    .replace('\t', ''))
        activity_name = (str(raw_activity['name'])
                         .replace(',', '')
                         .replace('\n', '')
                         .replace('\t', ''))

        activity = Activity(
            athlete_id=raw_activity['athlete']['id'],
            athlete_name=fullname,
            name=activity_name,
            distance=raw_activity['distance'],
            moving_time=raw_activity['moving_time'],
            total_elevation_gain=raw_activity['total_elevation_gain'],
            type=raw_activity['type'],
            sport_type=raw_activity['sport_type'],
            start_date_local=raw_activity['start_date_local'],
            achievement_count=raw_activity['achievement_count'],
            kudos_count=raw_activity['kudos_count'],
            comment_count=raw_activity['comment_count'],
            athlete_count=raw_activity['athlete_count'],
            photo_count=raw_activity['total_photo_count']
        )

        activities.append(activity)

    # Writing activities to activity file
    with open(f"{config.activities_folder}/activities.csv", 'a', encoding="utf-8") as activities_file:
        for activity in activities:
            line = (f"{activity.athlete_id},{activity.athlete_name},{activity.name},"
                    f"{activity.distance},{activity.moving_time},{activity.total_elevation_gain},{activity.type},"
                    f"{activity.sport_type},{activity.start_date_local},{activity.achievement_count},"
                    f"{activity.kudos_count},{activity.comment_count},{activity.athlete_count},"
                    f"{activity.photo_count}")

            activities_file.write(line + "\n")

    # Wait for rate limit
    sleep(2)


def get_all_user_year_activities():
    athletes = get_all_athletes()

    for athlete in athletes:
        firstname = athlete[0]
        lastname = athlete[1]
        refresh_token = athlete[2]

        get_user_year_activities(firstname=firstname, lastname=lastname, refresh_token=refresh_token)


def close_connection(conn):
    if conn:
        conn.close()


if __name__ == "__main__":
    # get_all_user_year_activities()

    print(get_access_token(get_refresh_token(15376382)))

atexit.register(close_connection, connection)
