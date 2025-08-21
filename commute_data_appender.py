import csv
import os
from datetime import datetime
from commute_time import get_commute_time
from config import ApartmentLocation, WorkLocation
from zoneinfo import ZoneInfo

def append_commute_snapshot(api_key: str, csv_path: str = "commute_data.csv") -> None:
    time_pst = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d %H:%M:%S %Z")

    rows = []
    for apt in ApartmentLocation:
        for work in WorkLocation:
            apartment_to_work = get_commute_time(origin=apt.value, destination=work.value, api_key=api_key)
            work_to_apartment = get_commute_time(origin=work.value, destination=apt.value, api_key=api_key)

            rows.append([
                time_pst,
                apt.name,
                work.name,
                apartment_to_work.duration_minutes if apartment_to_work else "",
                work_to_apartment.duration_minutes if work_to_apartment else "",
            ])

    header = ["TimePST", "apartment", "workplace", "apartmentToWorkplace", "workplaceToApartment"]
    # Create file with header if missing/empty; otherwise append
    needs_header = not os.path.exists(csv_path) or os.stat(csv_path).st_size == 0
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if needs_header:
            writer.writerow(header)
        writer.writerows(rows)
