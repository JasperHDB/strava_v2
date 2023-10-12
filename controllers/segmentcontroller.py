import config
import http.client
import json
from time import sleep
from controllers.athletecontroller import get_access_token

stravahttpconnection = http.client.HTTPSConnection("www.strava.com")


def get_athlete_segment_efforts(firstname, lastname, refresh_token):
    if not refresh_token or not firstname or not lastname:
        return print("Invalid arguments")

    print(f"\nFetching segment efforts of {firstname} {lastname}")

    access_token = get_access_token(refresh_token)

    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    for segment in config.strava_segments:
        print(f"Fetching efforts of {segment['name']}")
        stravahttpconnection.request("GET",
                                     f"/api/v3/segment_efforts?segment_id={segment['id']}"
                                     f"&per_page={config.per_page}"
                                     f"&start_date_local={config.low_iso}"
                                     f"&end_date_local={config.high_iso}",
                                     headers=headers)

        raw_efforts = json.loads(stravahttpconnection.getresponse().read())

        # Check if the user has a free tier account
        if "message" in raw_efforts and "errors" in raw_efforts:
            print("Payment is required")
            return

        efforts = len(raw_efforts)

        print(f"Efforts found: {efforts}")

        # Writing activities to activity file
        with open(f"{config.segments_folder}/{segment['name']}.csv", 'a', encoding="utf-8") as outfile:
            outfile.write(f"{firstname},{lastname},{efforts}\n")

        sleep(1)
