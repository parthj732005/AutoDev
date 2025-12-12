import os
from datetime import datetime

LOG_FILE = "app/logs/run.log"

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    print(entry.strip())  

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
