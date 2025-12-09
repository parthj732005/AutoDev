import os
from openai import OpenAI

HF_API_KEY = os.getenv("HF_API_KEY", "")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_KEY,
)

MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct:nscale"


def call_llm(prompt: str, max_tokens: int = 800) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a senior software engineer."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.2,
    )

    return response.choices[0].message.content
