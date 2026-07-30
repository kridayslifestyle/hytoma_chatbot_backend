from sqlalchemy.orm import Session
from app.models.conversation import Conversation


def save_message(
        db: Session,
        customer_id: str,
        role: str,
        message: str):

    conversation = Conversation(
        customer_id=customer_id,
        role=role,
        message=message
    )

    db.add(conversation)
    db.commit()


def get_history(
        db,
        customer_id,
        limit=10):

    messages = (
        db.query(Conversation)
        .filter(
            Conversation.customer_id == customer_id
        )
        .order_by(
            Conversation.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    messages.reverse()

    return messages