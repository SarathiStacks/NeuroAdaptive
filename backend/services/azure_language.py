import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-15-preview"
)

def check_understanding(text: str) -> str:
    prompt = f"""
A student read the following passage:

{text}

Give short, kind feedback in simple language.
Do not quiz or judge.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a supportive reading tutor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=120
    )

    return response.choices[0].message.content
