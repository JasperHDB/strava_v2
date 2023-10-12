# Strava Club Activity & SegmentEffort Fetcher

This is a simple Python script that uses the Strava API to fetch activities and segment efforts of users in a 
Strava club, and writes them to corresponding CSV files.

This project was initially created for private use to address a specific need. 
It was not originally intended for public distribution so my code might be rough.

## Prerequisites

- Create a Strava application if it's not created yet
- You should have a postgresql table with user data. An example is ddl.sql
- Make sure you have a Python 3.8 environment enabled.
- Install the required packages `pip install -r requirements.txt`

## Usage

1. Clone this repository or download the script.

2. Open the config.py file and enter your basic configuration
    
3. Create a .env file and enter your credentials as in the example .env file

4. Run `python setup_csv_files.py` to set up your configured directories and files.

To run the main script:

`python main.py`

- The script will fetch activities from the specified Strava club and save them to a file named activities.csv in your configured directory for activities.
- The segment efforts will be saved as {segment_name}.csv in your configured directory for segments.

To reset the data:

Run `python setup_csv_files.py` again

## Sample Output

The activities file will contain a list of activities with the following columns:

    athlete_id
    athlete_name
    name
    distance
    moving_time
    total_elevation_gain
    type
    sport_type
    start_date_local
    achievement_count
    kudos_count
    comment_count
    athlete_count
    photo_count

The segment efforts files will contain a list of segment efforts with the following columns:

    firstname
    lastname
    attempts

### Note

Make sure to keep your CLIENT_ID and CLIENT_SECRET private. Do not share them publicly.
This script uses the Strava API, so you may need to authenticate with your Strava account when you run it for the first time.