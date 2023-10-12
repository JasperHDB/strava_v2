# Begin Epoch for activities (current: Sunday, January 1, 2023 1:00:00 AM GMT+01:00)
low_epoch = 1672531200
low_iso = "2023-01-01T00:00:00.000Z"
# End Epoch for activities (current: Monday, January 1, 2024 12:59:59 AM GMT+01:00)
high_epoch = 1704067199
high_iso = "2023-12-31T23:59:59.000Z"

# The limit of activities that are called at once, cannot exceed 200 due to Strava limitations
activity_limit = 200

data_folder = "./data"
segments_folder = f"{data_folder}/segments"
activities_folder = f"{data_folder}/activities"

# Names of segments of the analysis
strava_segments = [
    "GVO_op_woensdag",
    "Safir_FVT",
    "Safir_DVDV",
    "Safir_AnjaV",
    "Safir_TDS",
    "Safir_BVM"
]
