from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class SkillMatch(BaseModel):
    skill: str
    status: Literal["found", "missing", "partial"]
    weight: Literal["required", "preferred"]

class ScoreBreakdown(BaseModel):
    skills_required: int
    skills_preferred: int
    experience: int
    education: int
    presentation: int

class AnalysisResult(BaseModel):
    global_score: int
    breakdown: ScoreBreakdown
    skills_analysis: list[SkillMatch]
    strengths: list[str]
    improvements: list[str]

class AnalysisHistoryItem(BaseModel):
    id: str
    job_title: str | None = None
    global_score: int
    created_at: datetime
