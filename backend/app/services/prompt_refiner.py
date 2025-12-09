from app.services.llm_client import call_llm


def refine_prompt(
    original_prompt: str,
    work_item: dict,
    detected_patterns: list[str],
    user_feedback: list[str],
):
    """
    Improves prompts using:
    - Azure DevOps work item
    - Detected patterns
    - User feedback
    """

    meta_prompt = f"""
You are a prompt engineering expert.

Your task is to improve a system prompt so future
code generation better satisfies the requirements.

Original Prompt:
{original_prompt}

Work Item:
Title: {work_item.get('title')}
Description: {work_item.get('description')}

Detected Patterns:
{detected_patterns}

User Feedback:
{user_feedback}

Rules:
- Keep prompt concise
- Encode constraints explicitly
- Avoid mentioning specific framework versions
- Make prompt reusable for similar tasks

Return ONLY the improved prompt.
"""

    return call_llm(meta_prompt, max_tokens=250)
