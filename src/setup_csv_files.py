import os
import config


def setup_csv_files():
    try:
        if not os.path.isdir(config.data_folder):
            os.mkdir(config.data_folder)
            os.mkdir(config.segments_folder)
            os.mkdir(config.activities_folder)

        # Creating the segments files and filling in the headers
        for segment in config.strava_segments:
            os.remove(f"{config.segments_folder}/{segment}.csv") \
                if os.path.isfile(f"{config.segments_folder}/{segment}.csv") \
                else print(f"Creating {segment}.csv")

            # Filling in the headers of the segment file
            with open(f"{config.segments_folder}/{segment}.csv", "w") as writefile:
                writefile.write("firstname,lastname,attempts\n")
            print(f"Refreshed {segment}.csv")

        # Creating the activities file
        os.remove(f"{config.activities_folder}/activities.csv") \
            if os.path.isfile(f"{config.activities_folder}/activities.csv") \
            else print(f"Creating activities.csv")

        # Filling in the headers of the activities file
        with open(f"{config.activities_folder}/activities.csv", "w") as writefile:
            writefile.write("athlete_id,athlete_name,name,distance,moving_time,total_elevation_gain,type,sport_type,"
                            "start_date_local,achievement_count,kudos_count,comment_count,athlete_count,photo_count\n")
            print(f"Refreshed activities.csv")

        print("Success :)")
    except Exception as error:
        print("Something went wrong :(")
        print(error)


if __name__ == '__main__':
    setup_csv_files()
