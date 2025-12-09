RULES = {
    "jwt": "Always include JWT authentication",
    "tailwind": "Use Tailwind CSS for UI",
}

def refine_prompt(prompt: str, feedback: list[str]):
    for f in feedback:
        for k, rule in RULES.items():
            if k in f.lower():
                prompt += f"\nNOTE: {rule}"

    return prompt
