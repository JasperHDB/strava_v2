import http.client
import json
import os
import psycopg2
from time import sleep
from dotenv import load_dotenv
from activity import Activity

stravaconnection = http.client.HTTPSConnection("www.strava.com")

LOW_EPOCH = 1672531200
HIGH_EPOCH = 1704067199

ACTIVITY_LIMIT = 200

data_folder = "./data"
segments_folder = f"{data_folder}/segments"
activities_folder = f"{data_folder}/activities"

load_dotenv('.env')

try:
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"))
    print("\nConnected to the database successfully!\n")
except psycopg2.Error as e:
    print("Error connecting to the database:", e)
    exit()

cursor = connection.cursor()


def get_all_athletes():
    cursor.execute("SELECT firstname, lastname, refresh_token FROM strava.users")
    rows = cursor.fetchall()

    if len(rows) == 0:
        print(f"No users were found")

    return rows


def get_access_token(refresh_token):
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
    """
    cursor.execute("SELECT refresh_token FROM strava.users WHERE strava_athlete_id = %s", (athlete_id,))
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
        return print("Invalid arguments")

    print(f"\nGetting activities of {firstname} {lastname}")

    access_token = get_access_token(refresh_token)

    print(f"Fetching activities with token {access_token}")

    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    page = 1
    per_page = 200
    fetched_data = []

    while True:
        stravaconnection.request("GET",
                                 f"/api/v3/athlete/activities?after={LOW_EPOCH}"
                                 f"&before={HIGH_EPOCH}"
                                 f"&page={page}"
                                 f"&per_page={per_page}",
                                 headers=headers)

        raw_activities = json.loads(stravaconnection.getresponse().read())

        if len(raw_activities) == 0:
            print(f"Stopping on page nr. {page}")
            break

        print(f"Adding data on page nr. {page}")
        fetched_data.extend(raw_activities)
        page += 1

    print(f"Activities found: {len(fetched_data)}")

    if len(fetched_data) != 0:
        activities = []

        print(f"Cleaning up activities")
        for raw_activity in fetched_data:
            fullname = f"{firstname} {lastname}"
            activity_name = str(raw_activity['name'])
            activity_name = activity_name.replace(',', '')
            activity_name = activity_name.replace('\n', '')
            activity_name = activity_name.replace('\t', '')

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

        print(f"Writing activities")
        with open(f"{activities_folder}/activities.csv", 'a', encoding="utf-8") as activities_file:
            for activity in activities:
                line = (f"{activity.athlete_id},{activity.athlete_name},{activity.name},"
                        f"{activity.distance},{activity.moving_time},{activity.total_elevation_gain},{activity.type},"
                        f"{activity.sport_type},{activity.start_date_local},{activity.achievement_count},{activity.kudos_count},"
                        f"{activity.comment_count},{activity.athlete_count},{activity.photo_count}")

                activities_file.write(line + "\n")

        print(f"Done, logged {len(activities)} from {firstname} {lastname}")
    else:
        print(f"Skipping {firstname} {lastname}")

    sleep(2)


def get_all_user_year_activities():
    athletes = get_all_athletes()

    for athlete in athletes:
        firstname = athlete[0]
        lastname = athlete[1]
        refresh_token = athlete[2]

        get_user_year_activities(firstname=firstname, lastname=lastname, refresh_token=refresh_token)


if __name__ == "__main__":
    get_all_user_year_activities()

    cursor.close()
    connection.close()
