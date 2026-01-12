import json
import re
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-15-preview"
)


def _safe_json(text: str):
    match = re.search(r"\[\s*{.*?}\s*\]", text, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON found")
    return json.loads(match.group())


def generate_quiz(topic: str, difficulty: str):
    prompt = f"""
Topic: {topic}
Difficulty: {difficulty}

Generate EXACTLY 5 MCQ questions.
Return ONLY valid JSON:

[
  {{
    "question": "string",
    "options": ["A", "B", "C", "D"],
    "answer": 0
  }}
]
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate quizzes for ADHD learners. JSON ONLY."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    try:
        return _safe_json(response.choices[0].message.content)
    except Exception:
        # failsafe quiz (never crash demo)
        return [
            {
                "question": "What is 2 + 2?",
                "options": ["1", "2", "3", "4"],
                "answer": 3
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Earth", "Mars", "Jupiter", "Venus"],
                "answer": 1
            },
            {
                "question": "What gas do plants absorb?",
                "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
                "answer": 2
            },
            {
                "question": "Which is a programming language?",
                "options": ["Python", "Snake", "Lizard", "Cobra"],
                "answer": 0
            },
            {
                "question": "What is the capital of India?",
                "options": ["Mumbai", "Delhi", "Chennai", "Kolkata"],
                "answer": 1
            }
        ]


def generate_explanations(wrong_answers: list):
    """
    Generates simple explanations for wrong answers (ADHD-friendly)
    """
    if not wrong_answers:
        return []

    prompt = f"""
Explain why the correct answers are correct in a short,
friendly, ADHD-friendly way.

Questions:
{json.dumps(wrong_answers, indent=2)}

Return ONLY JSON list:
[
  {{
    "question": "...",
    "explanation": "..."
  }}
]
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You explain quiz answers simply and clearly."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400
    )

    try:
        return _safe_json(response.choices[0].message.content)
    except Exception:
        # fallback explanations
        return [
            {
                "question": w["question"],
                "explanation": "Review the concept and focus on why the correct option best fits."
            }
            for w in wrong_answers
        ]
