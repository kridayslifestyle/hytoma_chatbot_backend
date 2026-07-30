from sqlalchemy.orm import Session
from app.models.conversation_summary import ConversationSummary


def get_summary(
        db: Session,
        customer_id: str):

    return (
        db.query(
            ConversationSummary
        )
        .filter(
            ConversationSummary.customer_id == customer_id
        )
        .first()
    )


def save_summary(
        db: Session,
        customer_id: str,
        summary_text: str):

    summary = get_summary(
        db,
        customer_id
    )

    if summary:

        summary.summary = summary_text

        summary.version += 1

    else:

        summary = ConversationSummary(
            customer_id=customer_id,
            summary=summary_text
        )

        db.add(summary)

    db.commit()