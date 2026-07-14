from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.analyze.schemas import AnalysisHistoryItem, AnalysisResult
from app.analyze.service import analyze_resume, get_analysis_detail, get_analysis_history
from app.dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze", response_model=AnalysisResult)
async def analyze(
    job_description: str = Form(...),
    cv: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
) -> AnalysisResult:
    if cv.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF")

    cv_bytes = await cv.read()
    return analyze_resume(job_description, cv_bytes, current_user["sub"])


@router.get("/analyze/history", response_model=list[AnalysisHistoryItem])
async def history(current_user: dict = Depends(get_current_user)) -> list[AnalysisHistoryItem]:
    return get_analysis_history(current_user["sub"])


@router.get("/analyze/history/{analysis_id}", response_model=AnalysisResult)
async def history_detail(
    analysis_id: str, current_user: dict = Depends(get_current_user)
) -> AnalysisResult:
    return get_analysis_detail(current_user["sub"], analysis_id)
