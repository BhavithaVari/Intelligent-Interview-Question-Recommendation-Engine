"""
Generates interview questions using Groq AI
"""
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print("Loaded API Key:", api_key)

client = Groq(api_key=api_key)

SYSTEM_PROMPT = """You are an expert technical interviewer. Return ONLY valid JSON,
no markdown fences, no preamble, no explanation outside the JSON."""

PROMPT_TEMPLATE = """Based on the candidate's resume and job description, generate 5 interview questions.

Candidate's matched skills: {strengths}
Candidate's missing/unclear skills: {gaps}
Job description summary: {jd_text}
Resume summary: {resume_text}

Rules:
- Cover: required technical skills, project experience, missing skills, and practical problem-solving
- Assign each question a difficulty: Easy, Medium, or Hard
- No duplicate questions
- Each question must include expected_answer_points (3-6 points) and a reason

Return this exact JSON shape:
{{
  "questions": [
    {{
      "question": "...",
      "difficulty": "Easy | Medium | Hard",
      "expected_answer_points": ["...", "..."],
      "reason": "..."
    }}
  ]
}}
"""

def generate_questions(strengths, gaps, jd_text, resume_text) -> dict:
    prompt = PROMPT_TEMPLATE.format(
        strengths=", ".join(strengths) or "none identified",
        gaps=", ".join(gaps) or "none identified",
        jd_text=jd_text[:2000],
        resume_text=resume_text[:2000],
    )
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
        response_format={"type": "json_object"},
    )
    
    raw = response.choices[0].message.content.strip()
    
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"questions": [], "error": "Failed to parse AI response", "raw": raw}