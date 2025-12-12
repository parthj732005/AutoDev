from app.services.task_parser import detect_patterns

def decompose_story(story):
    return ["BACKEND", "FRONTEND", "DATABASE"]

def confidence_low(patterns: list[str]) -> bool:
    return len(patterns) == 0

