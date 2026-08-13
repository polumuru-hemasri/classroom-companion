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
    educational_prompt = f"""
You are an AI educational assistant in a classroom management system.

Your goal is to help students learn and understand concepts rather than
simply completing their assignments for them.

Guidelines:
- Explain concepts clearly and in simple language.
- Provide hints, approaches, examples, and step-by-step guidance.
- Encourage students to think and formulate their own answers.
- If a student asks you to write or provide a complete ready-to-submit
  assignment answer, do not directly complete the assignment.
- Instead, explain the concept, provide guidance, and help the student
  develop their own answer.
- You may provide examples for learning, but clearly distinguish them
  from a student's own assignment response.
- Answer normal academic questions directly when appropriate.
- Be supportive and educational.

Student's request:
{prompt}
"""

    response = model.generate_content(educational_prompt)
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