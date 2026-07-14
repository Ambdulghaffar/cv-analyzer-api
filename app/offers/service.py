from datetime import datetime, timezone

from fastapi import HTTPException

from app.core.supabase_client import get_supabase
from app.offers.schemas import JobOffer, JobOfferCreate, JobOfferUpdate


def create_offer(recruiter_id: str, data: JobOfferCreate) -> JobOffer:
    supabase = get_supabase()
    response = (
        supabase.table("job_offers")
        .insert({"recruiter_id": recruiter_id, **data.model_dump()})
        .execute()
    )
    return JobOffer.model_validate(response.data[0])


def list_offers(recruiter_id: str) -> list[JobOffer]:
    supabase = get_supabase()
    response = (
        supabase.table("job_offers")
        .select("*")
        .eq("recruiter_id", recruiter_id)
        .order("created_at", desc=True)
        .execute()
    )
    return [JobOffer.model_validate(row) for row in response.data]


def get_offer(recruiter_id: str, offer_id: str) -> JobOffer:
    supabase = get_supabase()
    response = (
        supabase.table("job_offers")
        .select("*")
        .eq("id", offer_id)
        .eq("recruiter_id", recruiter_id)
        .maybe_single()
        .execute()
    )
    if not response or not response.data:
        raise HTTPException(status_code=404, detail="Offre introuvable")
    return JobOffer.model_validate(response.data)


def update_offer(recruiter_id: str, offer_id: str, data: JobOfferUpdate) -> JobOffer:
    get_offer(recruiter_id, offer_id)

    supabase = get_supabase()
    update_data = data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    response = (
        supabase.table("job_offers")
        .update(update_data)
        .eq("id", offer_id)
        .eq("recruiter_id", recruiter_id)
        .execute()
    )
    return JobOffer.model_validate(response.data[0])


def delete_offer(recruiter_id: str, offer_id: str) -> None:
    get_offer(recruiter_id, offer_id)

    supabase = get_supabase()
    supabase.table("job_offers").delete().eq("id", offer_id).eq(
        "recruiter_id", recruiter_id
    ).execute()
