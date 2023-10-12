import os

# Begin Epoch for activities (current: Sunday, January 1, 2023 1:00:00 AM GMT+01:00)
low_epoch = 1672531200
low_iso = "2023-01-01T00:00:00.000Z"
# End Epoch for activities (current: Monday, January 1, 2024 12:59:59 AM GMT+01:00)
high_epoch = 1704067199
high_iso = "2023-12-31T23:59:59.000Z"

# The limit of data that is called at once, cannot exceed 200 due to Strava limitations
per_page = 200

root = os.path.dirname(os.path.abspath(__file__))
data_folder = f"{root}/data"
segments_folder = f"{data_folder}/segments"
activities_folder = f"{data_folder}/activities"

# Names of segments of the analysis
strava_segments = [
    {"id": 23897602, "name": "GVO_op_woensdag"},
    {"id": 33400402, "name": "Safir_FVT"},
    {"id": 33400458, "name": "Safir_DVDV"},
    {"id": 33423218, "name": "Safir_AnjaV"},
    {"id": 33470695, "name": "Safir_TDS"},
    {"id": 33470960, "name": "Safir_BVM"}
]
