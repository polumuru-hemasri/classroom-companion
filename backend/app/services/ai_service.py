import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def ask_gemini(prompt):

    response = model.generate_content(
        prompt
    )

    return response.text
def extract_assignment_details(text):

    prompt = f"""
Extract the information below.

Instruction:
{text}

Return ONLY exactly like this:

Student:Hemasri
Assignment:500-word essay on AI
Deadline:30 June 2026
"""

    response = model.generate_content(prompt)

    return response.text
def extract_progress(text):

    prompt = f"""
Extract progress information.

Instruction:
{text}

Return ONLY in this format:

Progress: <percentage>

Status: One of these:
Pending
In Progress
Completed
"""

    response = model.generate_content(prompt)

    return response.text
def review_submission(text):

    prompt = f"""
You are a teacher.

Review the student's assignment submission.

Submission:
{text}

Provide:

Strengths:
- ...

Areas for Improvement:
- ...

Suggested Feedback:
...
"""

    response = model.generate_content(
        prompt
    )

    return response.text