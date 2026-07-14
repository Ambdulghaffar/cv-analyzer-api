from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.analyze.service import extract_text_from_pdf
from app.dependencies import get_current_user
from app.letters.schemas import LetterResult
from app.letters.service import generate_letter

router = APIRouter(prefix="/api", tags=["letters"])


@router.post("/generate-letter", response_model=LetterResult)
async def generate(
    job_description: str = Form(...),
    tone: str = Form("professionnel"),
    language: str = Form("français"),
    cv: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
) -> LetterResult:
    if cv.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF")

    cv_bytes = await cv.read()
    resume_text = extract_text_from_pdf(cv_bytes)
    return generate_letter(job_description, resume_text, tone, language)
