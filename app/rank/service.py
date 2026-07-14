import json
import logging

from fastapi import HTTPException
from pydantic import ValidationError

from app.analyze.service import extract_text_from_pdf, get_ai_analysis
from app.core.supabase_client import get_supabase
from app.rank.schemas import CandidateRanking, RankingHistoryItem, RankingResult

logger = logging.getLogger(__name__)

MAX_CANDIDATES = 10


def rank_candidates(
    job_description: str, cv_files: list[tuple[str, bytes]], user_id: str
) -> RankingResult:
    if len(cv_files) > MAX_CANDIDATES:
        raise HTTPException(
            status_code=400,
            detail=f"Trop de fichiers : {MAX_CANDIDATES} CVs maximum par classement",
        )

    candidates: list[CandidateRanking] = []

    for filename, cv_bytes in cv_files:
        resume_text = extract_text_from_pdf(cv_bytes)

        try:
            analysis = get_ai_analysis(job_description, resume_text)
        except (json.JSONDecodeError, ValidationError):
            try:
                analysis = get_ai_analysis(job_description, resume_text)
            except (json.JSONDecodeError, ValidationError):
                logger.error(
                    "Échec de l'analyse du CV '%s', exclu du classement", filename
                )
                continue

        candidates.append(CandidateRanking(filename=filename, analysis=analysis))

    candidates.sort(key=lambda c: c.analysis.global_score, reverse=True)

    result = RankingResult(candidates=candidates)

    supabase = get_supabase()
    supabase.table("ranking_sessions").insert(
        {
            "user_id": user_id,
            "job_description": job_description,
            "results": [candidate.model_dump() for candidate in candidates],
        }
    ).execute()

    return result


def get_ranking_history(user_id: str, limit: int = 20) -> list[RankingHistoryItem]:
    supabase = get_supabase()
    response = (
        supabase.table("ranking_sessions")
        .select("id, results, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return [
        RankingHistoryItem(
            id=row["id"],
            candidate_count=len(row.get("results") or []),
            created_at=row["created_at"],
        )
        for row in response.data
    ]


def get_ranking_detail(user_id: str, session_id: str) -> RankingResult:
    supabase = get_supabase()
    response = (
        supabase.table("ranking_sessions")
        .select("*")
        .eq("id", session_id)
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )
    if not response or not response.data:
        raise HTTPException(status_code=404, detail="Classement introuvable")
    return RankingResult(candidates=response.data["results"])
