from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt: str, max_tokens=400):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a senior software engineer."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
    )

    return {
        "role": "assistant",
        "content": response.choices[0].message.content
    }
