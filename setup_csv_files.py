import os

segments = [
    "GVO_op_woensdag",
    "Safir_FVT",
    "Safir_DVDV",
    "Safir_AnjaV",
    "Safir_TDS",
    "Safir_BVM"
]

data_folder = "./data"
segments_folder = f"{data_folder}/segments"
activities_folder = f"{data_folder}/activities"


def setup_csv_files():
    try:
        if not os.path.isdir(data_folder):
            os.mkdir(data_folder)
            os.mkdir(segments_folder)
            os.mkdir(activities_folder)

        # Creating the segments files and filling in the headers
        for segment in segments:
            os.remove(f"{segments_folder}/{segment}.csv") if os.path.isfile(f"{segments_folder}/{segment}.csv")\
                else print(f"Creating {segment}.csv")

            # Filling in the headers of the segment file
            with open(f"{segments_folder}/{segment}.csv", "w") as writefile:
                writefile.write("voornaam,achternaam,pogingen\n")
            print(f"Refreshed {segment}.csv")

        # Creating the activities file
        os.remove(f"{activities_folder}/activities.csv") if os.path.isfile(f"{activities_folder}/activities.csv")\
            else print(f"Creating activities.csv")

        # Filling in the headers of the activities file
        with open(f"{activities_folder}/activities.csv", "w") as writefile:
            writefile.write("athlete_id,athlete_name,name,distance,moving_time,total_elevation_gain,type,sport_type,"
                            "start_date_local,achievement_count,kudos_count,comment_count,athlete_count,photo_count\n")
            print(f"Refreshed activities.csv")

        print("Success :)")
    except Exception as error:
        print("Something went wrong :(")
        print(error)


if __name__ == '__main__':
    setup_csv_files()
