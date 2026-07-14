import io
import json

import pdfplumber
from fastapi import HTTPException
from groq import Groq
from pydantic import ValidationError

from app.config import settings
from app.core.supabase_client import get_supabase
from app.analyze.prompts import SYSTEM_PROMPT, build_user_prompt
from app.analyze.schemas import AnalysisHistoryItem, AnalysisResult

groq_client = Groq(api_key=settings.groq_api_key)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def get_ai_analysis(job_description: str, resume_text: str) -> AnalysisResult:
    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(job_description, resume_text)},
        ],
    )
    raw_content = completion.choices[0].message.content
    data = json.loads(raw_content)
    return AnalysisResult.model_validate(data)


def analyze_resume(job_description: str, cv_bytes: bytes, user_id: str) -> AnalysisResult:
    resume_text = extract_text_from_pdf(cv_bytes)

    try:
        result = get_ai_analysis(job_description, resume_text)
    except (json.JSONDecodeError, ValidationError):
        try:
            result = get_ai_analysis(job_description, resume_text)
        except (json.JSONDecodeError, ValidationError):
            raise HTTPException(
                status_code=500, detail="Erreur lors de l'analyse, veuillez réessayer"
            )

    supabase = get_supabase()
    supabase.table("analyses").insert(
        {
            "user_id": user_id,
            "job_description": job_description,
            "global_score": result.global_score,
            "breakdown": result.breakdown.model_dump(),
            "skills_analysis": [skill.model_dump() for skill in result.skills_analysis],
            "strengths": result.strengths,
            "improvements": result.improvements,
        }
    ).execute()

    return result


def get_analysis_history(user_id: str, limit: int = 20) -> list[AnalysisHistoryItem]:
    supabase = get_supabase()
    response = (
        supabase.table("analyses")
        .select("id, job_title, global_score, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return [AnalysisHistoryItem.model_validate(row) for row in response.data]


def get_analysis_detail(user_id: str, analysis_id: str) -> AnalysisResult:
    supabase = get_supabase()
    response = (
        supabase.table("analyses")
        .select("*")
        .eq("id", analysis_id)
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )
    if not response or not response.data:
        raise HTTPException(status_code=404, detail="Analyse introuvable")
    return AnalysisResult.model_validate(response.data)
