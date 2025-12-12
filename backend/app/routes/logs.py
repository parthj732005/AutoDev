from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import time
import os

router = APIRouter()

LOG_FILE = "app/logs/run.log"


def stream_logs():
    last_size = 0

    # Create file if not exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()

    while True:
        current_size = os.path.getsize(LOG_FILE)

        # If new content is added
        if current_size > last_size:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                f.seek(last_size)
                new_lines = f.read()
                yield f"data: {new_lines}\n\n"
            last_size = current_size

        time.sleep(0.4)  # smoother updates


@router.get("/stream")
def logs_stream():
    return StreamingResponse(stream_logs(), media_type="text/event-stream")
