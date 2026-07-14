from pydantic import BaseModel
from datetime import datetime
from app.analyze.schemas import AnalysisResult

class CandidateRanking(BaseModel):
    filename: str
    analysis: AnalysisResult

class RankingResult(BaseModel):
    job_title: str | None = None
    candidates: list[CandidateRanking]

class RankingHistoryItem(BaseModel):
    id: str
    job_title: str | None = None
    candidate_count: int
    created_at: datetime
