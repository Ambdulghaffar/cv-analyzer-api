from pydantic import BaseModel
from datetime import datetime

class JobOfferCreate(BaseModel):
    title: str
    description: str

class JobOfferUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class JobOffer(BaseModel):
    id: str
    recruiter_id: str
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
