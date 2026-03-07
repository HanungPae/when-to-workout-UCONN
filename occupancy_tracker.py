import requests
import csv
from datetime import datetime
import os

URL = "https://app.safespace.io/api/display/live-occupancy/86fb9e11?view=percent"
FILE = "data.csv"

# 1. The Disguise: Tell the server we are a normal Chrome browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 2. Make the request with the headers
r = requests.get(URL, headers=HEADERS)

# 3. Safety check: Did the server give us a 200 OK success code?
if r.status_code == 200:
    try:
        percent = r.json()["percent"]
        now = datetime.utcnow().isoformat()
        
        file_exists = os.path.isfile(FILE)
        
        with open(FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "percent"])
            writer.writerow([now, percent])
            
        print(f"Success! Logged {percent}% at {now}")
        
    except Exception as e:
        print("Error: The server returned a 200 OK, but the data wasn't JSON.")
        print("Here is what the server actually sent back:")
        print(r.text)
else:
    print(f"Failed to connect! The server returned status code: {r.status_code}")
    print("Here is the error message from the server:")
    print(r.text)
