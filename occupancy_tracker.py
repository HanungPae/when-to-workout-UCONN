import requests
import csv
from datetime import datetime
import os

URL = "https://app.safespace.io/api/display/live-occupancy/86fb9e11?view=percent"
FILE = "data.csv"

r = requests.get(URL)
percent = r.json()["percent"]

now = datetime.utcnow().isoformat()

file_exists = os.path.isfile(FILE)

with open(FILE, "a", newline="") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow(["timestamp", "percent"])

    writer.writerow([now, percent])
