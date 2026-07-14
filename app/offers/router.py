from fastapi import APIRouter, Depends, HTTPException, status

from app.core.supabase_client import get_supabase
from app.dependencies import get_current_user
from app.offers.schemas import JobOffer, JobOfferCreate, JobOfferUpdate
from app.offers.service import (
    create_offer,
    delete_offer,
    get_offer,
    list_offers,
    update_offer,
)

router = APIRouter(prefix="/api/offers", tags=["offers"])


def _extract_role_from_claims(current_user: dict) -> str | None:
    app_metadata = current_user.get("app_metadata") or {}
    user_metadata = current_user.get("user_metadata") or {}
    return app_metadata.get("role") or user_metadata.get("role")


def require_recruiter(current_user: dict = Depends(get_current_user)) -> dict:
    role = _extract_role_from_claims(current_user)

    if role is None:
        supabase = get_supabase()
        response = (
            supabase.table("profiles")
            .select("role")
            .eq("id", current_user["sub"])
            .single()
            .execute()
        )
        role = response.data["role"] if response.data else None

    if role != "recruiter":
        raise HTTPException(status_code=403, detail="Réservé aux recruteurs")

    return current_user


@router.post("/", response_model=JobOffer)
async def create(
    data: JobOfferCreate, current_user: dict = Depends(require_recruiter)
) -> JobOffer:
    return create_offer(current_user["sub"], data)


@router.get("/", response_model=list[JobOffer])
async def list_all(current_user: dict = Depends(require_recruiter)) -> list[JobOffer]:
    return list_offers(current_user["sub"])


@router.get("/{offer_id}", response_model=JobOffer)
async def get_one(
    offer_id: str, current_user: dict = Depends(require_recruiter)
) -> JobOffer:
    return get_offer(current_user["sub"], offer_id)


@router.patch("/{offer_id}", response_model=JobOffer)
async def update(
    offer_id: str,
    data: JobOfferUpdate,
    current_user: dict = Depends(require_recruiter),
) -> JobOffer:
    return update_offer(current_user["sub"], offer_id, data)


@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(offer_id: str, current_user: dict = Depends(require_recruiter)) -> None:
    delete_offer(current_user["sub"], offer_id)
