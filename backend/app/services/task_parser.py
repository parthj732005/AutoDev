import re

PATTERNS = {
    "AUTH": ["login", "signup", "authentication"],
    "CRUD": ["create", "update", "delete", "list"],
    "ENTITY": ["user", "order", "product", "task"],
    "API": ["api", "endpoint", "service"],
    "UI": ["ui", "page", "form"],
    "DB": ["database", "schema", "table"],
    "TEST": ["test", "validate"]
}

def detect_patterns(text: str):
    text = text.lower()
    found = []

    for pattern, keywords in PATTERNS.items():
        if any(k in text for k in keywords):
            found.append(pattern)

    return found
