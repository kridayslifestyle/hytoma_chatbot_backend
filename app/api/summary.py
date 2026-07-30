from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.summary_service import get_summary

router = APIRouter()


@router.get("/summary/{customer_id}")
def customer_summary(
        customer_id: str,
        db: Session = Depends(get_db)):

    summary = get_summary(
        db,
        customer_id
    )

    if summary:

        return {

            "customer_id": customer_id,

            "summary": summary.summary,

            "version": summary.version,

            "updated_at": summary.updated_at

        }

    return {
        "message": "No summary found"
    }