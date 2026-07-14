from app.analyze.service import groq_client
from app.letters.prompts import LETTER_SYSTEM_PROMPT, build_letter_prompt
from app.letters.schemas import LetterResult


def generate_letter(job_description: str, resume_text: str, tone: str, language: str) -> LetterResult:
    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        messages=[
            {"role": "system", "content": LETTER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_letter_prompt(job_description, resume_text, tone, language),
            },
        ],
    )
    content = completion.choices[0].message.content
    return LetterResult(content=content)
