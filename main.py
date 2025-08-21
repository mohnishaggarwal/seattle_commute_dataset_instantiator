import os
from commute_data_appender import append_commute_snapshot
from datetime import datetime
import pytz

def main():
    tz = pytz.timezone("America/Los_Angeles")
    now = datetime.now(tz)
    # Skip if weekend (Saturday=5, Sunday=6) or between 9 PM or 6 AM
    if now.weekday() in (5, 6) or now.hour >= 21 or now.hour < 6:
        exit(0)

    api_key = os.environ["GOOGLE_MAPS_API_KEY"]
    path_to_data_set = "/Users/amohnish/PycharmProjects/CommuteTracker/commute_data.csv"
    append_commute_snapshot(api_key, path_to_data_set)
    exit(0)

if __name__ == "__main__":
    main()
