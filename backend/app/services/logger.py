import queue
import time

log_queue = queue.Queue()

def log(message: str):
    timestamped = f"[{time.strftime('%H:%M:%S')}] {message}"

    # write to file (safe for demo)
    with open("app/logs/run.log", "a") as f:
        f.write(timestamped + "\n")

    # push to live stream
    log_queue.put(timestamped)
