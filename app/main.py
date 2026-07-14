from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.dependencies import get_current_user
from app.analyze.router import router as analyze_router
from app.rank.router import router as rank_router
from app.offers.router import router as offers_router
from app.letters.router import router as letters_router

app = FastAPI(title="CV Analyzer API")

app.include_router(analyze_router)
app.include_router(rank_router)
app.include_router(offers_router)
app.include_router(letters_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/me")
async def me(current_user: dict = Depends(get_current_user)):
    return {"user_id": current_user["sub"], "email": current_user.get("email")}