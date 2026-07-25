import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_mcqs(subject, topic_or_pdf, difficulty, exam_type, num_questions):

    # If a large amount of text is received, assume it came from a PDF
    if len(topic_or_pdf) > 500:

        prompt = f"""
You are an expert exam paper setter.

Generate {num_questions} multiple choice questions ONLY from the study notes below.

Subject:
{subject}

Study Notes:
{topic_or_pdf}

Difficulty:
{difficulty}

Exam Type:
{exam_type}

Instructions:

- Questions MUST come only from the provided notes.
- Do not use outside knowledge.
- Each question must have exactly 4 options.
- Only one correct answer.
- Include a short explanation.
- Return ONLY valid JSON.

Format:

[
  {{
    "question":"Question",
    "options":["A","B","C","D"],
    "answer":"Correct Option",
    "explanation":"Explanation"
  }}
]
"""

    else:

        prompt = f"""
Generate {num_questions} MCQs.

Subject:
{subject}

Topic:
{topic_or_pdf}

Difficulty:
{difficulty}

Exam Type:
{exam_type}

Instructions:

- Exactly 4 options.
- One correct answer.
- Short explanation.
- Return ONLY valid JSON.

Format:

[
  {{
    "question":"Question",
    "options":["A","B","C","D"],
    "answer":"Correct Option",
    "explanation":"Explanation"
  }}
]
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    try:
        return json.loads(text)

    except Exception:

        return [{
            "question": "AI Response Error",
            "options": [
                "Try Again",
                "Check API",
                "Check Prompt",
                "Restart App"
            ],
            "answer": "Try Again",
            "explanation": text
        }]