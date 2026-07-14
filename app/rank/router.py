from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.dependencies import get_current_user
from app.rank.schemas import RankingHistoryItem, RankingResult
from app.rank.service import get_ranking_detail, get_ranking_history, rank_candidates

router = APIRouter(prefix="/api", tags=["rank"])


@router.post("/rank", response_model=RankingResult)
async def rank(
    job_description: str = Form(...),
    cvs: list[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user),
) -> RankingResult:
    for cv in cvs:
        if cv.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail=f"Le fichier '{cv.filename}' doit être un PDF",
            )

    cv_files = [(cv.filename, await cv.read()) for cv in cvs]

    return rank_candidates(job_description, cv_files, current_user["sub"])


@router.get("/rank/history", response_model=list[RankingHistoryItem])
async def history(current_user: dict = Depends(get_current_user)) -> list[RankingHistoryItem]:
    return get_ranking_history(current_user["sub"])


@router.get("/rank/history/{session_id}", response_model=RankingResult)
async def history_detail(
    session_id: str, current_user: dict = Depends(get_current_user)
) -> RankingResult:
    return get_ranking_detail(current_user["sub"], session_id)
