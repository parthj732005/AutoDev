from app.services.task_parser import detect_patterns

def decompose_story(story: dict):
    patterns = detect_patterns(story["title"] + " " + story.get("description", ""))

    tasks = []

    if "API" in patterns or "AUTH" in patterns:
        tasks.append("BACKEND")

    if "UI" in patterns:
        tasks.append("FRONTEND")

    if "DB" in patterns:
        tasks.append("DATABASE")

    if "TEST" in patterns:
        tasks.append("TESTING")

    return tasks

def confidence_low(patterns: list[str]) -> bool:
    return len(patterns) == 0

