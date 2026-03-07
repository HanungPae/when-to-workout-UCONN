from playwright.sync_api import sync_playwright
import csv
from datetime import datetime
import os

URL = "https://app.safespace.io/api/display/live-occupancy/86fb9e11?view=percent"
FILE = "data.csv"

# Start the invisible browser
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    try:
        # Go to the TV display page
        page.goto(URL)
        
        # Wait up to 10 seconds for the websocket to push the number to the screen
        page.wait_for_selector("#occupancyPct", state="visible", timeout=10000)
        
        # Grab the text (e.g., "45%")
        percent_text = page.locator("#occupancyPct").inner_text()
        
        # Clean it up to just be an integer (e.g., 45)
        percent = int(percent_text.replace('%', '').strip())
        
        now = datetime.utcnow().isoformat()
        file_exists = os.path.isfile(FILE)
        
        # Save to CSV
        with open(FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "percent"])
            writer.writerow([now, percent])
            
        print(f"Success! Logged {percent}% at {now}")
        
    except Exception as e:
        print("Failed to scrape the data. The page might have changed or failed to load.")
        print(e)
    finally:
        browser.close()
